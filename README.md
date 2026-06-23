# SecureFin Authentication System
A secure User Authentication and Authorization module built with Python and Flask for SecureFin Sdn. Bhd.

## Group Members
- Mauloof Mohamed Abdulla
- Lim Guan You
- Muhammad Afrin Faris bin Abu Samah
- Ying Lei

## Technologies Used
- Python 3.13
- Flask
- Flask-SQLAlchemy (SQLite database)
- Flask-JWT-Extended (JWT token authentication)
- bcrypt (password hashing)

## Project Structure
SSS_GP_Assignment/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   └── templates/
├── instance/
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourrepo/securefin-auth.git
cd securefin-auth
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Configure environment variables
Create a `.env` file in the root folder:
```
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
DATABASE_URL=sqlite:///securefin.db
```

### 4. Run the application
```bash
python run.py
```
The database will be created automatically and the app will be available at `http://127.0.0.1:5000`

## API Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /auth/register | Register a new user | No |
| POST | /auth/login | Login and receive JWT token | No |
| POST | /auth/logout | Invalidate current token | Yes |
| GET | /auth/profile | View current user profile | Yes |
| GET | /admin/users | List all users (admin only) | Yes (Admin) |

## Security Configuration
- Passwords are hashed using bcrypt (cost factor 12) before storage
- JWT tokens expire after 15 minutes
- Refresh tokens expire after 7 days
- All database queries use parameterised statements via SQLAlchemy
- Input validation is applied on all user-supplied fields
- Secure error handling — no stack traces exposed to the client
- TLS should be enabled in production via a reverse proxy (e.g. Nginx)
- Never commit your `.env` file — it is listed in `.gitignore`

## OWASP ASVS Compliance

| # | Requirement | Implementation |
|---|-------------|----------------|
| V2.1 | Secure password storage | bcrypt with cost factor 12 |
| V2.4 | No credential exposure in errors | Generic error messages returned |
| V3.1 | Session token generation | JWT via Flask-JWT-Extended |
| V5.1 | Input validation | Validated on all endpoints |
| V7.1 | Secure logging | Logs exclude sensitive data |
| V14.1 | Parameterised queries | SQLAlchemy ORM used throughout |

## Running Security Tests

### SAST (Static Analysis)
```bash
pip install bandit
bandit -r . -f txt -o bandit_report.txt
```

### DAST (Dynamic Analysis)
1. Start the Flask app with `flask run`
2. Open OWASP ZAP
3. Set target to `http://127.0.0.1:5000`
4. Run Active Scan
5. Export report as HTML

### Unit & Abuse Case Tests
```bash
pip install pytest
pytest tests/ -v
```

## Dependencies
```
bcrypt==5.0.0
blinker==1.9.0
click==8.4.1
colorama==0.4.6
Flask==3.1.3
Flask-JWT-Extended==4.7.4
Flask-SQLAlchemy==3.1.1
greenlet==3.5.2
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
PyJWT==2.13.0
SQLAlchemy==2.0.51
typing_extensions==4.15.0
Werkzeug==3.1.8
```

## Development Dependencies
python-dotenv==1.0.0
pytest==7.4.0
bandit==1.7.7

## Known Limitations
- SQLite is used for development only; switch to PostgreSQL for production
- TLS not configured locally; must be set up via reverse proxy in production
- MFA not implemented in this prototype

## Academic Declaration
This project was developed as part of ITS69405 Software Secure Systems at Taylor's University. All code is the original work of the group. Any external references have been cited in the final report.