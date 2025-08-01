from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime
import json
import time
from dotenv import load_dotenv
from models import Consultation, ConsultationStorage
from security import rate_limit, get_client_ip, sanitize_input, generate_session_id

# Load environment variables from .env file
load_dotenv()

# Initialize storage
consultation_storage = ConsultationStorage()

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('legal_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=[
    "http://127.0.0.1:5000", 
    "http://localhost:5000",
    "http://127.0.0.1:5501",  # Live Server
    "http://localhost:5501"
])

# Professional configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Initialize OpenAI client with enhanced error handling
client = None
try:
    from openai import OpenAI
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        client = OpenAI(api_key=api_key)
        logger.info("✅ OpenAI client initialized successfully")
    else:
        logger.warning("WARNING: No OpenAI API key found. Running in demo mode.")
        
except ImportError:
    logger.error("❌ OpenAI package not installed. Please install: pip install openai")
    client = None
except Exception as e:
    logger.error(f"❌ Error initializing OpenAI client: {e}")
    client = None

# Professional legal categories and expertise areas
LEGAL_CATEGORIES = {
    "criminal": "Criminal Law (IPC, CrPC)",
    "civil": "Civil Law (CPC, Contract Act)",
    "constitutional": "Constitutional Law",
    "corporate": "Corporate & Business Law",
    "family": "Family & Personal Law",
    "property": "Property & Real Estate Law",
    "labor": "Labor & Employment Law",
    "tax": "Tax & Revenue Law",
    "intellectual": "Intellectual Property Law",
    "cyber": "Cyber Law & IT Act"
}

# Serve frontend files
@app.route('/')
def serve_frontend():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory('static', filename)

@app.route('/api/v1/legal-consultation', methods=['POST'])
@rate_limit(max_requests=5, window_minutes=1)  # 5 requests per minute
def legal_consultation():
    """
    Professional legal consultation endpoint
    Provides AI-powered legal analysis for Indian law queries
    """
    try:
        # Enhanced request validation
        if not request.json:
            return jsonify({
                "status": "error",
                "message": "Invalid request format. JSON required.",
                "timestamp": datetime.now().isoformat()
            }), 400
            
        query = request.json.get('query', '').strip()
        category = request.json.get('category', 'general')
        urgency = request.json.get('urgency', 'normal')
        
        if not query:
            return jsonify({
                "status": "error",
                "message": "Legal query is required.",
                "timestamp": datetime.now().isoformat()
            }), 400
            
        if len(query) < 10:
            return jsonify({
                "status": "error",
                "message": "Please provide a more detailed legal query (minimum 10 characters).",
                "timestamp": datetime.now().isoformat()
            }), 400
            
        logger.info(f"📋 Legal consultation request - Category: {category}, Urgency: {urgency}")
        logger.info(f"📝 Query: {query[:100]}...")

        if client:
            try:
                # Professional AI prompt for legal analysis
                system_prompt = """You are a Senior Legal Advisor specializing in Indian Law with 15+ years of experience. 
                Provide professional, accurate, and well-structured legal analysis following Indian legal framework.
                
                Always include:
                - Legal Status Assessment
                - Applicable Laws & Sections
                - Professional Recommendations
                - Next Steps
                - Important Disclaimers
                
                Maintain professional tone and cite relevant legal provisions."""
                
                user_prompt = f"""
                Legal Category: {LEGAL_CATEGORIES.get(category, 'General Legal Matter')}
                Urgency Level: {urgency.title()}
                
                CLIENT QUERY:
                {query}
                
                Please provide a comprehensive legal analysis in the following professional format:
                
                **LEGAL STATUS ASSESSMENT:**
                [Clear assessment of the legal standing]
                
                **APPLICABLE LAWS & SECTIONS:**
                [Relevant Indian laws, acts, and specific sections]
                
                **PROFESSIONAL ANALYSIS:**
                [Detailed legal analysis and implications]
                
                **RECOMMENDED ACTIONS:**
                [Specific, actionable legal steps]
                
                **TIMELINE & URGENCY:**
                [Time-sensitive considerations if any]
                
                **IMPORTANT DISCLAIMERS:**
                [Professional legal disclaimers]
                """

                response = client.chat.completions.create(
                    model="gpt-4" if urgency == "urgent" else "gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.3,
                    presence_penalty=0.1
                )

                legal_analysis = response.choices[0].message.content
                
                logger.info("✅ AI legal analysis generated successfully")
                
                return jsonify({
                    "status": "success",
                    "data": {
                        "legal_analysis": legal_analysis,
                        "consultation_id": f"LC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "category": category,
                        "urgency": urgency,
                        "ai_model": "gpt-4" if urgency == "urgent" else "gpt-3.5-turbo"
                    },
                    "metadata": {
                        "response_time": "AI-powered",
                        "disclaimer": "This is AI-generated legal guidance. Consult a qualified lawyer for official legal advice.",
                        "timestamp": datetime.now().isoformat()
                    }
                })
                
            except Exception as openai_error:
                logger.error(f"❌ OpenAI API error: {openai_error}")
                
        # Professional demo response when AI is unavailable
        demo_analysis = f"""
**LEGAL STATUS ASSESSMENT:**
Your query regarding "{query[:50]}..." requires professional legal consultation for accurate assessment.

**APPLICABLE LAWS & SECTIONS:**
Multiple Indian legal provisions may apply including:
- Indian Penal Code (IPC) 1860
- Code of Criminal Procedure (CrPC) 1973
- Indian Contract Act 1872
- Constitution of India 1950
- Specific Acts based on case nature

**PROFESSIONAL ANALYSIS:**
This matter falls under {LEGAL_CATEGORIES.get(category, 'General Legal')} and requires detailed case-specific analysis by a qualified legal professional to provide accurate guidance.

**RECOMMENDED ACTIONS:**
1. Consult with a licensed advocate specializing in {category} law
2. Gather all relevant documents and evidence
3. Consider legal precedents in similar cases
4. Evaluate jurisdiction and applicable court procedures

**TIMELINE & URGENCY:**
Urgency Level: {urgency.title()}
Recommended consultation timeframe: {"Immediate" if urgency == "urgent" else "Within 7-10 days"}

**IMPORTANT DISCLAIMERS:**
- This is a demo legal analysis system
- Always consult qualified legal professionals for official advice
- Laws and procedures may vary based on jurisdiction
- Time-sensitive matters require immediate professional consultation
        """
        
        logger.info("ℹ️ Providing professional demo legal analysis")
        
        return jsonify({
            "status": "success",
            "data": {
                "legal_analysis": demo_analysis,
                "consultation_id": f"DEMO_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "category": category,
                "urgency": urgency,
                "ai_model": "demo_mode"
            },
            "metadata": {
                "response_time": "Instant",
                "disclaimer": "Demo mode active. For AI-powered analysis, configure OpenAI API key.",
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Server error in legal consultation: {e}")
        return jsonify({
            "status": "error",
            "message": "Internal server error. Please try again later.",
            "error_code": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Professional health check endpoint"""
    ai_status = "operational" if client else "demo_mode"
    
    return jsonify({
        "status": "healthy",
        "service": "Legal Bot API",
        "version": "1.0.0",
        "ai_status": ai_status,
        "uptime": "Service operational",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/api/v1/legal-consultation": "POST - Legal consultation service",
            "/api/v1/health": "GET - Service health check",
            "/api/v1/categories": "GET - Available legal categories"
        }
    })

@app.route('/api/v1/categories', methods=['GET'])
def get_legal_categories():
    """Get available legal categories"""
    return jsonify({
        "status": "success",
        "data": {
            "categories": LEGAL_CATEGORIES,
            "urgency_levels": ["normal", "urgent", "emergency"]
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/statistics', methods=['GET'])
def get_statistics():
    """Get consultation statistics"""
    try:
        stats = consultation_storage.get_stats()
        return jsonify({
            "status": "success",
            "data": stats,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({
            "status": "error",
            "message": "Unable to retrieve statistics",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/v1/feedback', methods=['POST'])
@rate_limit(max_requests=3, window_minutes=5)  # 3 feedback per 5 minutes
def submit_feedback():
    """Submit feedback for consultation"""
    try:
        if not request.json:
            return jsonify({
                "status": "error",
                "message": "Invalid request format. JSON required.",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        consultation_id = request.json.get('consultation_id', '')
        rating = request.json.get('rating', 0)
        feedback = sanitize_input(request.json.get('feedback', ''), 1000)
        
        if not consultation_id or not (1 <= rating <= 5):
            return jsonify({
                "status": "error",
                "message": "Valid consultation_id and rating (1-5) required.",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Store feedback (in a real app, you'd save this to database)
        feedback_data = {
            'consultation_id': consultation_id,
            'rating': rating,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat(),
            'ip': get_client_ip()
        }
        
        logger.info(f"Feedback received for consultation {consultation_id}: {rating}/5")
        
        return jsonify({
            "status": "success",
            "message": "Feedback submitted successfully",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    logger.info("Starting Professional Legal Bot API Server...")
    logger.info(f"Server URL: http://127.0.0.1:5000")
    logger.info(f"AI Status: {'OpenAI Ready' if client else 'Demo Mode'}")
    logger.info(f"Legal Categories: {len(LEGAL_CATEGORIES)} available")
    
    app.run(
        debug=False,
        host='127.0.0.1',
        port=5000,
        threaded=True
    )