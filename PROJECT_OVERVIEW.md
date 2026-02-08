# NoteMaster AI 

NoteMaster AI is a production-ready, AI-powered note summarization and study assistant built with Flask.
It transforms raw lecture notes or PDFs into structured summaries, enables contextual AI chat per note, and provides powerful organization tools such as tags, search, and history tracking.

This project was refactored from a basic prototype into a professional full-stack application following industry best practices in architecture, security, and UI/UX.

## Features

### Core Functionality
- AI-powered note summarization
- Context-aware chat per note
- Tag-based organization with custom colors
- Instant search across notes, summaries, and content
- PDF and TXT file upload support
- Full note and chat history

### User Experience
- Modern UI built with Tailwind CSS
- Dark mode optimized for studying
- Fully responsive (mobile, tablet, desktop)
- Loading indicators and empty states
- One-click copy to clipboard

### Reliability and Security
- Environment-based configuration (.env)
- No hardcoded API keys
- SQL injection protection via SQLAlchemy ORM
- File upload validation
- Graceful, user-friendly error handling

---

## Project Structure

```
notemaster-ai-pro/
├── app.py              # Application entry point
├── config.py           # Configuration management
├── models.py           # Database models
├── routes.py           # REST API endpoints
├── utils.py            # Utility/helper functions
├── templates/
│   └── index.html
├── static/
│   └── js/
│       └── script.js
├── instance/           # SQLite database storage
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Tech Stack

### Backend
- Flask
- SQLAlchemy
- PyPDF2
- python-dotenv
- Google Gemini API

### Frontend
- Tailwind CSS
- Vanilla JavaScript (ES6+)
- Font Awesome

### Database
- SQLite (default)
- PostgreSQL (production-ready option)

## Database Models

### Note
- id
- title
- original_content
- summary
- created_at
- updated_at
- tags (many-to-many)

### Tag
- id
- name (unique)
- color
- created_at

### ChatMessage
- id
- note_id
- role (user or assistant)
- content
- created_at

## API Endpoints

### Summarization
- POST /api/summarize

### Notes
- GET /api/notes
- GET /api/notes/<id>
- DELETE /api/notes/<id>

### Tags
- GET /api/tags
- POST /api/tags
- POST /api/notes/<id>/tags
- DELETE /api/notes/<id>/tags

### Chat
- GET /api/notes/<id>/chat
- POST /api/notes/<id>/chat

### Health
- GET /health

## Installation and Setup

### 1. Clone the repository
```
git clone https://github.com/your-username/notemaster-ai-pro.git
cd notemaster-ai-pro
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Configure environment variables
```
cp .env.example .env
```

Edit .env and add your API key:
```
GEMINI_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///notemaster.db
```

### 4. Run the application
```
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

---

## Future Enhancements

- User authentication (login/register)
- Note export (PDF, DOCX, Markdown)
- Sharing and collaboration
- Flashcard generation
- Spaced repetition system
- OCR for image-based notes
- Mobile app (iOS and Android)

---

## Learning Outcomes

This project demonstrates:
- Clean and scalable Flask architecture
- RESTful API design
- Relational database modeling
- Secure configuration management
- Modern frontend development
- Full-stack AI integration
- Production-focused engineering practices

---

## License

This project is for educational and portfolio purposes.
You are free to fork, modify, and extend it.

---

## Acknowledgments

- Flask and SQLAlchemy documentation
- Tailwind CSS
- Google Gemini API

# Author
Pearl Kristian M. Gardose
Start of Development: January 2026 
Uploaded: Febraury 2026
Status: Still developing
