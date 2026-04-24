🔐 API Security Scanner

A beginner-friendly command-line tool to scan API endpoints and identify common security misconfigurations.

🚀 Features
⚡ Concurrent scanning of multiple API endpoints
🔍 Checks HTTP status codes and authentication requirements
🛡️ Validates presence of essential security headers
🚨 Detects publicly exposed sensitive endpoints
🧵 Fast parallel execution using ThreadPoolExecutor
📦 Installation
Clone this repository:
```
git clone [https://github.com/your-username/api-security-scanner.git](https://github.com/vr8010/API-Security-Scanner-Python-)
cd api-security-scanner
```
Install dependencies:
```
pip install -r requirements.txt
```
▶️ Usage

Run the scanner:
```
python api_scanner.py
```
Input Prompts

Enter API base URL
Example:

https://api.example.com

Enter endpoints (comma-separated)
Example:

/users,/admin,/login
🧪 Example Output
=== API Security Scanner ===

Enter API base URL: https://api.example.com
Enter endpoints (comma separated): /users,/admin,/login

Scanning endpoints...

[+] /users
    Status Code: 200
    Auth Required: No
    Security Headers Missing: X-Frame-Options, Content-Security-Policy
    Warning: Public endpoint exposed

[+] /admin
    Status Code: 403
    Auth Required: Yes
    Security Headers: OK

[+] /login
    Status Code: 200
    Auth Required: No
    Security Headers Missing: Strict-Transport-Security

Scan Completed in 1.23 seconds.
🔍 Security Checks

This tool performs the following checks:

1. HTTP Status Codes
200 (OK)
401 (Unauthorized)
403 (Forbidden)
404 (Not Found)
500 (Server Error)
2. Authentication Detection
Identifies endpoints that require authentication
Flags publicly accessible sensitive endpoints
3. Security Headers Validation
Content-Security-Policy
X-Frame-Options
Strict-Transport-Security
X-Content-Type-Options
4. Misconfiguration Detection
Open admin panels (/admin)
Exposed login endpoints
Missing security protections
🧰 Tech Stack
Python 3.6+
requests
concurrent.futures (ThreadPoolExecutor)
📚 What You’ll Learn
Making HTTP requests using requests
Writing concurrent programs in Python
Basics of API security testing
Building CLI-based tools
⚠️ Disclaimer

This tool is intended for educational purposes and authorized security testing only.

❗ Do NOT scan APIs without proper permission.
Unauthorized scanning may be illegal.

💡 Future Improvements
Add support for authentication tokens (JWT, API keys)
Export results to JSON/CSV
Add rate-limit detection
Integrate vulnerability databases
