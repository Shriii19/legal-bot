"""
Enhanced monitoring and health check utilities
"""
import psutil
import time
from datetime import datetime
from typing import Dict, Any

class HealthMonitor:
    """System health monitoring"""
    
    def __init__(self):
        self.start_time = time.time()
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health information"""
        try:
            # System resources
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Uptime
            uptime_seconds = time.time() - self.start_time
            uptime_hours = uptime_seconds / 3600
            
            return {
                'system': {
                    'cpu_usage_percent': cpu_percent,
                    'memory_usage_percent': memory.percent,
                    'memory_available_mb': memory.available // 1024 // 1024,
                    'disk_usage_percent': disk.percent,
                    'disk_free_gb': disk.free // 1024 // 1024 // 1024
                },
                'application': {
                    'uptime_hours': round(uptime_hours, 2),
                    'uptime_seconds': round(uptime_seconds, 2),
                    'start_time': datetime.fromtimestamp(self.start_time).isoformat()
                },
                'status': 'healthy' if cpu_percent < 80 and memory.percent < 90 else 'warning'
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }

# Global health monitor instance
health_monitor = HealthMonitor()

def get_performance_metrics():
    """Get performance metrics"""
    return {
        'timestamp': datetime.now().isoformat(),
        'health': health_monitor.get_system_health()
    }
