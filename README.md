# 🏛️ LegalConsult Pro - AI Legal Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Professional AI-powered legal consultation system specializing in Indian Law**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Legal Categories](#legal-categories)
- [Security](#security)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

## 🎯 Overview

LegalConsult Pro is a sophisticated AI-powered legal assistant that provides professional legal analysis and consultation services for Indian law queries. The system combines modern web technologies with advanced AI to deliver accurate, well-structured legal guidance.

### 🌟 Key Highlights

- **AI-Powered Analysis**: Utilizes OpenAI's GPT models for intelligent legal analysis
- **Indian Law Specialization**: Focused on Indian legal framework and statutes
- **Professional Interface**: Clean, responsive web interface for seamless user experience
- **Comprehensive Coverage**: Supports 10+ legal categories
- **Secure & Private**: Environment-based configuration with security best practices

## ✨ Features

### 🤖 AI Legal Analysis
- **Intelligent Query Processing**: Advanced natural language understanding
- **Structured Responses**: Professional legal analysis format
- **Contextual Recommendations**: Actionable legal guidance
- **Urgency-Based Routing**: Priority handling for urgent matters

### 📚 Legal Expertise
- **Multi-Category Support**: Criminal, Civil, Corporate, Family law and more
- **Indian Law Focus**: IPC, CrPC, Constitution, Contract Act coverage
- **Case-Specific Analysis**: Tailored responses based on query context
- **Legal Citation**: Relevant law sections and precedents

### 🔧 Technical Features
- **RESTful API**: Clean, documented API endpoints
- **Real-time Processing**: Instant legal consultation responses
- **Error Handling**: Comprehensive error management and logging
- **Demo Mode**: Functional demo when AI is unavailable

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3.3** - Web framework
- **OpenAI API** - AI language model integration
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Modern markup
- **CSS3** - Advanced styling with CSS Grid/Flexbox
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Professional icons

### Infrastructure
- **Environment Variables** - Secure configuration management
- **Logging** - Comprehensive application logging
- **CORS** - Cross-origin request handling

## 📁 Project Structure

```
legal-bot/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── legal_bot.log         # Application logs
│   └── static/
│       └── index.html        # Frontend interface
├── frontend/
│   └── index.html            # Alternative frontend
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Root dependencies
├── BUG_FIXES_REPORT.md     # Bug fixes documentation
└── README.md               # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- OpenAI API key (optional for demo mode)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Shriii19/legal-bot.git
cd legal-bot
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Add your OpenAI API key (optional)
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

# Server Configuration
HOST=127.0.0.1
PORT=5000
```

### Configuration Options

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | No | Demo mode |
| `FLASK_ENV` | Flask environment mode | No | development |
| `SECRET_KEY` | Flask secret key | No | Auto-generated |
| `HOST` | Server host address | No | 127.0.0.1 |
| `PORT` | Server port number | No | 5000 |

## 🎮 Usage

### Starting the Server

```bash
# Navigate to backend directory
cd backend

# Start the Flask server
python app.py
```

The server will start at `http://127.0.0.1:5000`

### Using the Web Interface

1. **Open your browser** and navigate to `http://127.0.0.1:5000`
2. **Select legal category** from the dropdown menu
3. **Choose urgency level** (Normal, Urgent, Emergency)
4. **Enter your legal query** in the text area
5. **Click "Get Legal Consultation"** to receive AI analysis

### API Usage Example

```bash
curl -X POST http://127.0.0.1:5000/api/v1/legal-consultation \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "What are the legal requirements for starting a company in India?",
    "category": "corporate",
    "urgency": "normal"
  }'
```

## 📖 API Documentation

### Base URL
```
http://127.0.0.1:5000/api/v1
```

### Endpoints

#### POST `/legal-consultation`
Get AI-powered legal consultation

**Request Body:**
```json
{
  "query": "Your legal question",
  "category": "criminal|civil|corporate|family|...",
  "urgency": "normal|urgent|emergency"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "legal_analysis": "Detailed legal analysis...",
    "consultation_id": "LC_20250801_123456",
    "category": "corporate",
    "urgency": "normal",
    "ai_model": "gpt-3.5-turbo"
  },
  "metadata": {
    "response_time": "AI-powered",
    "disclaimer": "AI-generated guidance disclaimer",
    "timestamp": "2025-08-01T12:34:56"
  }
}
```

#### GET `/health`
Check service health status

#### GET `/categories`
Get available legal categories and urgency levels

## ⚖️ Legal Categories

| Category | Description | Indian Laws Covered |
|----------|-------------|-------------------|
| **Criminal** | Criminal Law matters | IPC, CrPC |
| **Civil** | Civil Law disputes | CPC, Contract Act |
| **Constitutional** | Constitutional matters | Constitution of India |
| **Corporate** | Business & Corporate law | Companies Act, SEBI |
| **Family** | Family & Personal law | Hindu Marriage Act, etc. |
| **Property** | Real Estate & Property | Transfer of Property Act |
| **Labor** | Employment & Labor law | Industrial Disputes Act |
| **Tax** | Taxation & Revenue | Income Tax Act, GST |
| **Intellectual** | IP & Patent law | Patents Act, Trademarks |
| **Cyber** | Cyber Law & IT | IT Act 2000 |

## 🔒 Security

### Security Features
- ✅ **Environment Variables**: Secure API key management
- ✅ **No Hardcoded Secrets**: All sensitive data in environment
- ✅ **CORS Protection**: Controlled cross-origin access
- ✅ **Input Validation**: Comprehensive request validation
- ✅ **Error Handling**: Secure error responses

### Security Best Practices
- Keep your `.env` file private (never commit to version control)
- Use strong, unique API keys
- Regularly rotate your OpenAI API keys
- Monitor API usage and costs
- Use HTTPS in production environments

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 Python style guide
- Add appropriate error handling
- Include docstrings for new functions
- Test your changes thoroughly
- Update documentation as needed

## ⚠️ Disclaimer

**IMPORTANT LEGAL DISCLAIMER:**

This application provides AI-generated legal information and guidance for educational and informational purposes only. It is NOT a substitute for professional legal advice from a qualified attorney.

### Key Points:
- 🔴 **Not Legal Advice**: Responses are informational only
- 🔴 **Consult Professionals**: Always consult qualified lawyers for legal matters
- 🔴 **No Attorney-Client Relationship**: Using this service does not create any legal relationship
- 🔴 **Accuracy Not Guaranteed**: AI responses may contain errors or be outdated
- 🔴 **Jurisdiction Specific**: Laws vary by location and time

**For actual legal matters, please consult with a licensed attorney in your jurisdiction.**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Shriii19/legal-bot/issues)
- **Documentation**: This README and inline code comments
- **Community**: Contribute via pull requests

## 🙏 Acknowledgments

- **OpenAI** for providing advanced language models
- **Flask** community for the excellent web framework
- **Indian Legal System** for the comprehensive legal framework
- **Open Source Community** for inspiration and best practices

---

<div align="center">

**Built with ❤️ for the Legal Community**

[⭐ Star this repo](https://github.com/Shriii19/legal-bot) | [🐛 Report Bug](https://github.com/Shriii19/legal-bot/issues) | [✨ Request Feature](https://github.com/Shriii19/legal-bot/issues)

</div>
