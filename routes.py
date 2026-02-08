from flask import Blueprint, render_template, request, jsonify, flash, current_app
from models import db, Note, Tag, ChatMessage
from utils import generate_summary, generate_chat_response, extract_text_from_pdf, generate_note_title, allowed_file
from sqlalchemy import or_

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@main.route('/api/summarize', methods=['POST'])
def summarize():
    """
    API endpoint to summarize notes using Gemini AI
    Accepts: JSON with 'notes' or file upload
    Returns: JSON with summary and note_id
    """
    try:
        notes_text = None
        
        # Check if it's a file upload
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type. Only PDF and TXT files are allowed.'}), 400
            
            # Extract text from PDF
            if file.filename.endswith('.pdf'):
                try:
                    notes_text = extract_text_from_pdf(file)
                except Exception as e:
                    return jsonify({'error': str(e)}), 400
            else:
                notes_text = file.read().decode('utf-8')
        
        # Check for JSON data
        elif request.is_json:
            data = request.get_json()
            if not data or 'notes' not in data:
                return jsonify({'error': 'No notes provided. Please enter some text to summarize.'}), 400
            notes_text = data['notes'].strip()
        
        else:
            return jsonify({'error': 'Invalid request format'}), 400
        
        # Validate input
        if len(notes_text) < current_app.config['NOTES_MIN_LENGTH']:
            return jsonify({
                'error': f'Notes are too short. Please enter at least {current_app.config["NOTES_MIN_LENGTH"]} characters.'
            }), 400
        
        if len(notes_text) > current_app.config['NOTES_MAX_LENGTH']:
            return jsonify({
                'error': f'Notes are too long. Please limit to {current_app.config["NOTES_MAX_LENGTH"]:,} characters.'
            }), 400
        
        # Generate summary
        try:
            summary = generate_summary(notes_text)
        except Exception as e:
            error_message = str(e)
            
            # Provide user-friendly error messages
            if 'API_KEY_INVALID' in error_message or 'API key not valid' in error_message:
                return jsonify({
                    'error': '🔑 Invalid API Key. Please check your Gemini API key in .env file'
                }), 401
            elif 'quota' in error_message.lower():
                return jsonify({
                    'error': '⚠️ API quota exceeded. Please try again later or check your Gemini API usage.'
                }), 429
            elif 'PERMISSION_DENIED' in error_message:
                return jsonify({
                    'error': '🚫 Permission denied. Please verify your API key has access to Gemini models.'
                }), 403
            else:
                return jsonify({
                    'error': f'⚠️ An error occurred: {error_message}'
                }), 500
        
        # Generate title and save to database
        title = generate_note_title(notes_text)
        
        note = Note(
            title=title,
            original_content=notes_text,
            summary=summary
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'summary': summary,
            'note_id': note.id,
            'title': title
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in summarize endpoint: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


@main.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes with optional filtering"""
    try:
        # Get query parameters
        tag_id = request.args.get('tag_id', type=int)
        search = request.args.get('search', '').strip()
        
        # Build query
        query = Note.query
        
        # Filter by tag
        if tag_id:
            query = query.filter(Note.tags.any(Tag.id == tag_id))
        
        # Search in title, content, or summary
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Note.title.ilike(search_pattern),
                    Note.original_content.ilike(search_pattern),
                    Note.summary.ilike(search_pattern)
                )
            )
        
        # Order by most recent
        notes = query.order_by(Note.created_at.desc()).all()
        
        return jsonify({
            'notes': [note.to_dict() for note in notes]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting notes: {e}")
        return jsonify({'error': str(e)}), 500


@main.route('/api/notes/<int:note_id>', methods=['GET', 'DELETE'])
def note_detail(note_id):
    """Get or delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        
        if request.method == 'GET':
            return jsonify(note.to_dict()), 200
        
        elif request.method == 'DELETE':
            db.session.delete(note)
            db.session.commit()
            return jsonify({'message': 'Note deleted successfully'}), 200
            
    except Exception as e:
        current_app.logger.error(f"Error with note {note_id}: {e}")
        return jsonify({'error': str(e)}), 500


@main.route('/api/notes/<int:note_id>/chat', methods=['POST'])
def chat_with_note(note_id):
    """Chat with AI about a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400
        
        user_question = data['question'].strip()
        
        if not user_question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Get chat history for this note
        chat_history = ChatMessage.query.filter_by(note_id=note_id).order_by(ChatMessage.created_at).all()
        chat_history_dict = [msg.to_dict() for msg in chat_history]
        
        # Generate AI response
        try:
            ai_response = generate_chat_response(
                note.original_content,
                note.summary,
                chat_history_dict,
                user_question
            )
        except Exception as e:
            return jsonify({'error': f'Error generating response: {str(e)}'}), 500
        
        # Save user question
        user_msg = ChatMessage(
            note_id=note_id,
            role='user',
            content=user_question
        )
        db.session.add(user_msg)
        
        # Save AI response
        ai_msg = ChatMessage(
            note_id=note_id,
            role='assistant',
            content=ai_response
        )
        db.session.add(ai_msg)
        
        db.session.commit()
        
        return jsonify({
            'response': ai_response,
            'user_message': user_msg.to_dict(),
            'ai_message': ai_msg.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500


@main.route('/api/notes/<int:note_id>/chat', methods=['GET'])
def get_chat_history(note_id):
    """Get chat history for a note"""
    try:
        note = Note.query.get_or_404(note_id)
        messages = ChatMessage.query.filter_by(note_id=note_id).order_by(ChatMessage.created_at).all()
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting chat history: {e}")
        return jsonify({'error': str(e)}), 500


@main.route('/api/tags', methods=['GET', 'POST'])
def tags():
    """Get all tags or create a new tag"""
    try:
        if request.method == 'GET':
            all_tags = Tag.query.order_by(Tag.name).all()
            return jsonify({
                'tags': [tag.to_dict() for tag in all_tags]
            }), 200
        
        elif request.method == 'POST':
            data = request.get_json()
            
            if not data or 'name' not in data:
                return jsonify({'error': 'Tag name is required'}), 400
            
            tag_name = data['name'].strip()
            
            if not tag_name:
                return jsonify({'error': 'Tag name cannot be empty'}), 400
            
            # Check if tag already exists
            existing_tag = Tag.query.filter_by(name=tag_name).first()
            if existing_tag:
                return jsonify({'error': 'Tag already exists'}), 400
            
            color = data.get('color', '#667eea')
            
            new_tag = Tag(name=tag_name, color=color)
            db.session.add(new_tag)
            db.session.commit()
            
            return jsonify(new_tag.to_dict()), 201
            
    except Exception as e:
        current_app.logger.error(f"Error with tags: {e}")
        return jsonify({'error': str(e)}), 500


@main.route('/api/notes/<int:note_id>/tags', methods=['POST', 'DELETE'])
def note_tags(note_id):
    """Add or remove tags from a note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.get_json()
        
        if not data or 'tag_id' not in data:
            return jsonify({'error': 'Tag ID is required'}), 400
        
        tag = Tag.query.get_or_404(data['tag_id'])
        
        if request.method == 'POST':
            if tag not in note.tags:
                note.tags.append(tag)
                db.session.commit()
                return jsonify({'message': 'Tag added successfully'}), 200
            else:
                return jsonify({'error': 'Tag already exists on this note'}), 400
        
        elif request.method == 'DELETE':
            if tag in note.tags:
                note.tags.remove(tag)
                db.session.commit()
                return jsonify({'message': 'Tag removed successfully'}), 200
            else:
                return jsonify({'error': 'Tag not found on this note'}), 400
                
    except Exception as e:
        current_app.logger.error(f"Error managing note tags: {e}")
        return jsonify({'error': str(e)}), 500


@main.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
