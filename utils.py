import google.generativeai as genai
from flask import current_app
import PyPDF2
from io import BytesIO


def configure_gemini():
    """Configure Gemini AI with API key"""
    try:
        api_key = current_app.config['GEMINI_API_KEY']
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in configuration")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(current_app.config['GEMINI_MODEL'])
        return model
    except Exception as e:
        current_app.logger.error(f"Error configuring Gemini AI: {e}")
        return None


def generate_summary(notes_text):
    """Generate a summary of the provided notes using Gemini AI"""
    model = configure_gemini()
    
    if not model:
        raise Exception("Gemini AI is not properly configured. Please check your API key.")
    
    prompt = f"""You are an expert study assistant. Analyze the following study notes and create a comprehensive, well-organized summary.

FORMATTING RULES (VERY IMPORTANT):
- Use bullet points with the • symbol (NOT asterisks *)
- Use proper HTML formatting for structure
- Use <strong> tags for emphasis (NOT **bold**)
- Use <em> tags for italics (NOT *italics*)
- Start each main point with •
- Organize related points together
- Be clear and concise

OUTPUT FORMAT:
Return your summary as clean HTML with:
- Main headings as <h3> tags
- Bullet points using • symbol
- Bold text using <strong> tags
- No markdown syntax (no *, **, _, __)
- No extra formatting characters

STUDY NOTES:
{notes_text}

SUMMARY:"""
    
    response = model.generate_content(prompt)
    
    if response and response.text:
        # Clean up any remaining asterisks or markdown
        summary = response.text.strip()
        
        # Replace common markdown with HTML
        summary = summary.replace('**', '')  # Remove bold asterisks
        summary = summary.replace('*', '•')  # Replace any remaining * with bullet
        summary = summary.replace('___', '')  # Remove underscores
        summary = summary.replace('__', '')
        summary = summary.replace('_', '')
        
        return summary
    else:
        raise Exception("No response received from Gemini AI")


def generate_chat_response(note_content, summary, chat_history, user_question):
    """Generate a chat response based on the note content and chat history"""
    model = configure_gemini()
    
    if not model:
        raise Exception("Gemini AI is not properly configured. Please check your API key.")
    
    # Build conversation context
    context = f"""You are a helpful AI study assistant. A student has taken notes and you've summarized them. Now they have a question about their notes.

FORMATTING RULES:
- Do NOT use asterisks (*) for formatting
- Use proper punctuation and grammar
- Be conversational and friendly
- Keep responses clear and concise
- No markdown formatting

ORIGINAL NOTES:
{note_content}

SUMMARY:
{summary}

CHAT HISTORY:
"""
    
    for msg in chat_history:
        role = "Student" if msg['role'] == 'user' else "Assistant"
        context += f"{role}: {msg['content']}\n"
    
    context += f"\nStudent: {user_question}\n\nAssistant:"
    
    response = model.generate_content(context)
    
    if response and response.text:
        # Clean up formatting
        reply = response.text.strip()
        
        # Remove markdown formatting
        reply = reply.replace('**', '')
        reply = reply.replace('*', '')
        reply = reply.replace('__', '')
        reply = reply.replace('_', '')
        
        return reply
    else:
        raise Exception("No response received from Gemini AI")


def extract_text_from_pdf(file_storage):
    """Extract text content from a PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_storage.read()))
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        if not text.strip():
            raise Exception("Could not extract text from PDF. The file may be empty or image-based.")
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")


def generate_note_title(content, max_length=50):
    """Generate a title from note content"""
    # Take first non-empty line or first 50 characters
    lines = content.strip().split('\n')
    first_line = next((line.strip() for line in lines if line.strip()), '')
    
    if first_line:
        title = first_line[:max_length]
        if len(first_line) > max_length:
            title += '...'
        return title
    else:
        return f"Note from {current_app.config.get('NOTES_MIN_LENGTH', 'date')}"


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']