from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for many-to-many relationship between notes and tags
note_tags = db.Table('note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class Note(db.Model):
    """Model for storing notes and their summaries"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    original_content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tags = db.relationship('Tag', secondary=note_tags, lazy='subquery',
                          backref=db.backref('notes', lazy=True))
    chat_messages = db.relationship('ChatMessage', backref='note', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'
    
    def to_dict(self):
        """Convert note to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'original_content': self.original_content,
            'summary': self.summary,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tags': [tag.to_dict() for tag in self.tags]
        }


class Tag(db.Model):
    """Model for categorizing notes"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), default='#667eea')  # Hex color code
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    def to_dict(self):
        """Convert tag to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }


class ChatMessage(db.Model):
    """Model for storing chat conversations about notes"""
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatMessage {self.id}: {self.role}>'
    
    def to_dict(self):
        """Convert message to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'note_id': self.note_id,
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }
