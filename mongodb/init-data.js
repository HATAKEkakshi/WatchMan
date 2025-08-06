// Initialize watchman database with bulk log data
db = db.getSiblingDB('watchman');

// Sample log data
const logs = [
  // Backend logs
  {service: "backend", level: "ERROR", message: "Database connection failed after 3 retries", metadata: "Connection timeout: 30s", timestamp: new Date()},
  {service: "backend", level: "ERROR", message: "SQL query execution failed", metadata: "table: users, error: connection_lost", timestamp: new Date()},
  {service: "backend", level: "ERROR", message: "Redis cache miss", metadata: "key: user_1234, fallback: db", timestamp: new Date()},
  {service: "backend", level: "ERROR", message: "Payment gateway timeout", metadata: "gateway: stripe, amount: $150", timestamp: new Date()},
  {service: "backend", level: "WARN", message: "High CPU usage detected", metadata: "usage: 85%, threshold: 80%", timestamp: new Date()},
  {service: "backend", level: "WARN", message: "Memory usage critical", metadata: "used: 6GB, available: 2GB", timestamp: new Date()},
  {service: "backend", level: "INFO", message: "User created successfully", metadata: "user_id: 5678, email: user5678@example.com", timestamp: new Date()},
  {service: "backend", level: "INFO", message: "Order processed", metadata: "order_id: 9876, amount: $299", timestamp: new Date()},
  
  // Auth logs
  {service: "auth", level: "ERROR", message: "Invalid login attempt detected", metadata: "username: user123, ip: 192.168.1.100", timestamp: new Date()},
  {service: "auth", level: "ERROR", message: "JWT token expired", metadata: "user_id: 4567, expired_at: 2024-01-15T10:30:00Z", timestamp: new Date()},
  {service: "auth", level: "ERROR", message: "Password reset failed", metadata: "email: user@example.com, reason: user_not_found", timestamp: new Date()},
  {service: "auth", level: "ERROR", message: "Account locked", metadata: "user_id: 7890, failed_attempts: 5", timestamp: new Date()},
  {service: "auth", level: "WARN", message: "Suspicious login activity", metadata: "user_id: 2345, location: Tokyo, ip: 10.0.0.25", timestamp: new Date()},
  {service: "auth", level: "WARN", message: "Multiple failed attempts", metadata: "username: user456, attempts: 3, window: 5min", timestamp: new Date()},
  {service: "auth", level: "INFO", message: "User logged in successfully", metadata: "user_id: 1234, session_id: sess_abc123", timestamp: new Date()},
  {service: "auth", level: "INFO", message: "Password changed", metadata: "user_id: 3456, timestamp: 2024-01-15T14:20:00Z", timestamp: new Date()},
  
  // Frontend logs
  {service: "frontend", level: "ERROR", message: "JavaScript runtime error in dashboard", metadata: "file: dashboard.js, line: 45, error: TypeError", timestamp: new Date()},
  {service: "frontend", level: "ERROR", message: "API call failed", metadata: "endpoint: /api/users, status: 500, retry: 2", timestamp: new Date()},
  {service: "frontend", level: "ERROR", message: "Component render failed", metadata: "component: UserCard, props: {id: 123}, stack: Error", timestamp: new Date()},
  {service: "frontend", level: "ERROR", message: "Image load failed", metadata: "src: /images/avatar.jpg, size: 150KB", timestamp: new Date()},
  {service: "frontend", level: "WARN", message: "Slow page load", metadata: "page: /dashboard, load_time: 5s, threshold: 3s", timestamp: new Date()},
  {service: "frontend", level: "WARN", message: "Memory leak detected", metadata: "component: Dashboard, memory: 85MB", timestamp: new Date()},
  {service: "frontend", level: "INFO", message: "Page loaded", metadata: "route: /profile, load_time: 1200ms, user_id: 789", timestamp: new Date()},
  {service: "frontend", level: "INFO", message: "User interaction", metadata: "action: click, element: button, user_id: 456", timestamp: new Date()}
];

// Insert bulk data
db.logs.insertMany(logs);

print("Inserted " + logs.length + " log entries into watchman database");