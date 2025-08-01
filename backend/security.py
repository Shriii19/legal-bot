"""
Security and rate limiting utilities
"""
import time
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import hashlib

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, max_requests=10, window_minutes=1):
        self.max_requests = max_requests
        self.window_seconds = window_minutes * 60
        self.requests = defaultdict(list)
    
    def is_allowed(self, identifier):
        """Check if request is allowed"""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] 
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False
    
    def get_reset_time(self, identifier):
        """Get time when rate limit resets"""
        if not self.requests[identifier]:
            return 0
        
        oldest_request = min(self.requests[identifier])
        return oldest_request + self.window_seconds

def rate_limit(max_requests=10, window_minutes=1):
    """Rate limiting decorator"""
    limiter = RateLimiter(max_requests, window_minutes)
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Use IP address as identifier
            identifier = request.remote_addr or 'unknown'
            
            if not limiter.is_allowed(identifier):
                reset_time = limiter.get_reset_time(identifier)
                return jsonify({
                    'status': 'error',
                    'message': 'Rate limit exceeded',
                    'reset_time': reset_time,
                    'timestamp': datetime.now().isoformat()
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers['X-Forwarded-For'].split(',')[0]
    elif request.headers.get('X-Real-IP'):
        return request.headers['X-Real-IP']
    else:
        return request.remote_addr

def sanitize_input(text, max_length=5000):
    """Sanitize user input"""
    if not text:
        return ''
    
    # Remove potential script tags and limit length
    text = str(text).strip()
    text = text.replace('<script>', '').replace('</script>', '')
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    
    return text[:max_length]

def generate_session_id():
    """Generate unique session ID"""
    timestamp = str(time.time())
    return hashlib.md5(timestamp.encode()).hexdigest()[:16]
