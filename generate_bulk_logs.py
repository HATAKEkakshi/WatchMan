import requests
import random
import time
from datetime import datetime, timedelta

API_URL = "http://localhost:8000/api/logs/"

# Log templates for different services
BACKEND_LOGS = [
    {"level": "ERROR", "message": "Database connection failed", "metadata": "timeout: {}s"},
    {"level": "ERROR", "message": "SQL query execution failed", "metadata": "table: users, error: {}"},
    {"level": "ERROR", "message": "Redis cache miss", "metadata": "key: user_{}, fallback: db"},
    {"level": "ERROR", "message": "Payment gateway timeout", "metadata": "gateway: stripe, amount: ${}"},
    {"level": "ERROR", "message": "File upload failed", "metadata": "size: {}MB, format: {}"},
    {"level": "WARN", "message": "High CPU usage detected", "metadata": "usage: {}%, threshold: 80%"},
    {"level": "WARN", "message": "Memory usage critical", "metadata": "used: {}GB, available: {}GB"},
    {"level": "WARN", "message": "Slow database query", "metadata": "duration: {}ms, query: SELECT"},
    {"level": "WARN", "message": "API rate limit approaching", "metadata": "requests: {}/1000"},
    {"level": "INFO", "message": "User created successfully", "metadata": "user_id: {}, email: user{}@example.com"},
    {"level": "INFO", "message": "Order processed", "metadata": "order_id: {}, amount: ${}"},
    {"level": "INFO", "message": "Email sent successfully", "metadata": "recipient: user{}@example.com, type: {}"},
    {"level": "INFO", "message": "Backup completed", "metadata": "size: {}GB, duration: {}min"},
    {"level": "DEBUG", "message": "Cache hit", "metadata": "key: session_{}, ttl: {}s"},
    {"level": "DEBUG", "message": "API request received", "metadata": "endpoint: /api/{}, method: {}"},
]

AUTH_LOGS = [
    {"level": "ERROR", "message": "Invalid login attempt", "metadata": "username: user{}, ip: 192.168.1.{}"},
    {"level": "ERROR", "message": "JWT token expired", "metadata": "user_id: {}, expired_at: {}"},
    {"level": "ERROR", "message": "Password reset failed", "metadata": "email: user{}@example.com, reason: {}"},
    {"level": "ERROR", "message": "OAuth callback failed", "metadata": "provider: {}, error: invalid_grant"},
    {"level": "ERROR", "message": "Account locked", "metadata": "user_id: {}, failed_attempts: {}"},
    {"level": "WARN", "message": "Suspicious login activity", "metadata": "user_id: {}, location: {}, ip: 10.0.0.{}"},
    {"level": "WARN", "message": "Multiple failed attempts", "metadata": "username: user{}, attempts: {}, window: 5min"},
    {"level": "WARN", "message": "Session timeout warning", "metadata": "user_id: {}, remaining: {}min"},
    {"level": "WARN", "message": "Weak password detected", "metadata": "user_id: {}, strength: {}/10"},
    {"level": "INFO", "message": "User logged in successfully", "metadata": "user_id: {}, session_id: sess_{}"},
    {"level": "INFO", "message": "Password changed", "metadata": "user_id: {}, timestamp: {}"},
    {"level": "INFO", "message": "Two-factor authentication enabled", "metadata": "user_id: {}, method: {}"},
    {"level": "INFO", "message": "User logged out", "metadata": "user_id: {}, session_duration: {}min"},
    {"level": "DEBUG", "message": "Token refreshed", "metadata": "user_id: {}, new_expiry: {}"},
    {"level": "DEBUG", "message": "Permission check", "metadata": "user_id: {}, resource: {}, allowed: {}"},
]

FRONTEND_LOGS = [
    {"level": "ERROR", "message": "JavaScript runtime error", "metadata": "file: {}.js, line: {}, error: {}"},
    {"level": "ERROR", "message": "API call failed", "metadata": "endpoint: /api/{}, status: {}, retry: {}"},
    {"level": "ERROR", "message": "Component render failed", "metadata": "component: {}, props: {}, stack: {}"},
    {"level": "ERROR", "message": "Form validation error", "metadata": "form: {}, field: {}, value: {}"},
    {"level": "ERROR", "message": "Image load failed", "metadata": "src: /images/{}.jpg, size: {}KB"},
    {"level": "WARN", "message": "Slow page load", "metadata": "page: /{}, load_time: {}s, threshold: 3s"},
    {"level": "WARN", "message": "Memory leak detected", "metadata": "component: {}, memory: {}MB"},
    {"level": "WARN", "message": "Deprecated API usage", "metadata": "api: {}, replacement: {}, version: {}"},
    {"level": "WARN", "message": "Large bundle size", "metadata": "bundle: {}.js, size: {}KB, limit: 500KB"},
    {"level": "INFO", "message": "Page loaded", "metadata": "route: /{}, load_time: {}ms, user_id: {}"},
    {"level": "INFO", "message": "User interaction", "metadata": "action: {}, element: {}, user_id: {}"},
    {"level": "INFO", "message": "Form submitted", "metadata": "form: {}, user_id: {}, success: {}"},
    {"level": "INFO", "message": "File downloaded", "metadata": "file: {}.pdf, size: {}MB, user_id: {}"},
    {"level": "DEBUG", "message": "State updated", "metadata": "component: {}, state: {}, trigger: {}"},
    {"level": "DEBUG", "message": "API response cached", "metadata": "endpoint: /api/{}, ttl: {}s, size: {}KB"},
]

def generate_metadata(template, service):
    """Generate realistic metadata based on template"""
    if service == "backend":
        replacements = [
            random.randint(5, 30),  # timeout
            random.choice(["connection_lost", "syntax_error", "permission_denied"]),
            random.randint(1000, 9999),  # user_id
            random.randint(10, 500),  # amount
            random.randint(1, 100),  # file size
            random.randint(70, 95),  # cpu usage
            random.randint(1, 8),   # memory used
            random.randint(2, 6),   # memory available
            random.randint(500, 5000),  # query duration
            random.randint(800, 999),   # rate limit
            random.choice(["welcome", "notification", "reminder"]),
            random.randint(10, 60),  # backup duration
            random.randint(300, 3600),  # ttl
            random.choice(["users", "orders", "products"]),
            random.choice(["GET", "POST", "PUT", "DELETE"])
        ]
    elif service == "auth":
        replacements = [
            random.randint(100, 255),  # ip
            datetime.now().isoformat(),
            random.choice(["user_not_found", "invalid_token", "expired"]),
            random.choice(["google", "facebook", "github"]),
            random.randint(3, 10),  # failed attempts
            random.choice(["New York", "London", "Tokyo", "Sydney"]),
            random.randint(1, 50),  # ip range
            random.randint(1, 10),  # password strength
            random.randint(15, 120),  # session duration
            random.choice(["SMS", "email", "authenticator"]),
            random.choice(["true", "false"])
        ]
    else:  # frontend
        replacements = [
            random.choice(["dashboard", "profile", "settings", "orders"]),
            random.randint(1, 200),  # line number
            random.choice(["TypeError", "ReferenceError", "SyntaxError"]),
            random.choice(["users", "orders", "products", "analytics"]),
            random.choice([404, 500, 502, 503]),
            random.randint(1, 3),  # retry count
            random.choice(["UserCard", "OrderList", "Dashboard", "Modal"]),
            random.choice(["email", "username", "password"]),
            random.choice(["avatar", "logo", "banner", "thumbnail"]),
            random.randint(50, 500),  # image size
            random.randint(3, 10),  # load time
            random.randint(10, 100),  # memory
            random.choice(["v1", "v2", "v3"]),
            random.randint(200, 800),  # bundle size
            random.randint(100, 2000),  # load time ms
            random.choice(["click", "scroll", "hover", "submit"]),
            random.choice(["button", "link", "input", "dropdown"]),
            random.choice(["report", "invoice", "export", "backup"]),
            random.randint(1, 50),  # file size MB
            random.choice(["loading", "error", "success"]),
            random.randint(60, 3600),  # cache ttl
            random.randint(1, 100)  # cache size
        ]
    
    # Replace placeholders in metadata
    try:
        return template.format(*replacements[:template.count("{}")])
    except:
        return template

def add_bulk_logs(count=200):
    """Add bulk demo logs"""
    services = ["backend", "auth", "frontend"]
    log_templates = {
        "backend": BACKEND_LOGS,
        "auth": AUTH_LOGS,
        "frontend": FRONTEND_LOGS
    }
    
    print(f"Adding {count} demo logs...")
    success_count = 0
    
    for i in range(count):
        service = random.choice(services)
        log_template = random.choice(log_templates[service])
        
        log_data = {
            "level": log_template["level"],
            "message": log_template["message"],
            "metadata": generate_metadata(log_template["metadata"], service)
        }
        
        try:
            response = requests.post(
                API_URL,
                json=log_data,
                headers={
                    "service": service,
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                success_count += 1
                if i % 20 == 0:  # Progress update every 20 logs
                    print(f"✅ Added {i+1}/{count} logs...")
            else:
                print(f"❌ Failed log {i+1}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error adding log {i+1}: {e}")
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    print(f"\n🎉 Bulk log generation complete!")
    print(f"📊 Successfully added: {success_count}/{count} logs")
    print(f"📈 Services: Backend, Auth, Frontend")
    print(f"📋 Log levels: ERROR, WARN, INFO, DEBUG")

if __name__ == "__main__":
    # Generate 200 logs by default, change as needed
    add_bulk_logs(200)