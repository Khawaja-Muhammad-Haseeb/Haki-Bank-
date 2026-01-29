# HakiBank - Online Banking Web Application

A complete, production-ready online banking system built with React and FastAPI.

## 🌟 Features

### User Features
- **Account Management** - Secure user accounts with role-based access
- **Initial Balance Setup** - Set starting balance when creating an account
- **Money Transfers** - Instant transfers to other accounts
- **Transaction History** - Detailed transaction records with filtering
- **Bill Payments** - Pay various utility bills
- **Profile Management** - Update personal information and change passwords
- **Dashboard Analytics** - Visual spending charts and account overview

### Admin Features
- **User Management** - View, edit, suspend, and delete user accounts
- **Transaction Monitoring** - Monitor all system transactions with filters
- **Dashboard Analytics** - System-wide statistics and metrics
- **Admin Action Logs** - Track all administrative actions

### Security
- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- HTTPS support ready
- SQL injection prevention
- CORS configuration

## 🛠️ Technology Stack

### Frontend
- React 18
- React Router v6
- Bootstrap 5
- Axios
- Chart.js
- Context API for state management

### Backend
- FastAPI (Python 3.9+)
- SQLAlchemy ORM
- PostgreSQL 14+
- JWT tokens (python-jose)
- Password hashing (passlib + bcrypt)
- Pydantic for validation

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL 14 or higher
- npm or yarn

## 🚀 Quick Start

### 1. Clone or Setup Project

```bash
cd bank
```

### 2. Database Setup

Create PostgreSQL database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE banking_db;

# Exit psql
\q
```

Run the database initialization script:

```bash
cd backend
python init_db.py
```

This will create all tables and seed initial data including:
- Admin user (admin@bank.com / admin123)
- Bill services

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy the following content to backend/.env:
APP_NAME=Online Banking System
VERSION=1.0.0
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/banking_db
SECRET_KEY=your-secret-key-change-this-in-production-use-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=["http://localhost:3000"]

# Run the server
python run.py
```

Backend will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will open at `http://localhost:3000`

## 🔐 Default Credentials

### Admin Account
- **Email:** admin@hakibank.com
- **Password:** admin123

**⚠️ IMPORTANT:** Change the admin password immediately after first login!

### Test User
Create a new user account through the signup page at `http://localhost:3000/signup`

## 📁 Project Structure

```
bank/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/        # API endpoints
│   │   │   └── deps.py        # Dependencies
│   │   ├── core/              # Core configuration
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── main.py           # FastAPI app
│   ├── init_db.py            # Database initialization
│   ├── run.py                # Server runner
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # Context providers
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── styles/           # CSS styles
│   │   ├── utils/            # Utility functions
│   │   ├── App.js           # Main app
│   │   └── index.js         # Entry point
│   └── package.json
│
├── database_schema.sql       # Database DDL
└── README.md
```

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user

### Users
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update profile
- `PUT /api/users/me/password` - Change password

### Accounts
- `GET /api/accounts/me` - Get user accounts
- `GET /api/accounts/me/balance` - Get balance

### Transactions
- `GET /api/transactions/me` - Get transactions
- `POST /api/transactions/transfer` - Transfer money
- `POST /api/transactions/withdraw` - Withdraw
- `POST /api/transactions/deposit` - Deposit (admin)

### Bills
- `GET /api/bills/services` - Get bill services
- `POST /api/bills/pay` - Pay bill

### Admin
- `GET /api/admin/stats` - Dashboard stats
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/:id` - Update user
- `DELETE /api/admin/users/:id` - Delete user
- `GET /api/admin/transactions` - All transactions
- `GET /api/admin/actions` - Admin action logs

## 🔧 Configuration

### Backend Configuration (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/banking_db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend Configuration

Edit `frontend/src/utils/constants.js`:

```javascript
export const API_BASE_URL = 'http://localhost:8000';
```

## 📊 Database Schema

The database includes:
- **users** - User accounts with roles
- **accounts** - Bank accounts
- **transactions** - All financial transactions
- **bill_services** - Available bill payment services
- **bill_payments** - Bill payment records
- **admin_actions** - Admin activity logs

See `database_schema.sql` for complete DDL.

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Production Deployment

### Backend
1. Set `DEBUG=False` in .env
2. Change `SECRET_KEY` to a strong random string
3. Update `DATABASE_URL` to production database
4. Use a production WSGI server (gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

### Frontend
1. Update `API_BASE_URL` in constants.js
2. Build production bundle:
   ```bash
   npm run build
   ```
3. Serve the `build` folder with nginx or another web server

### Database
1. Create production database
2. Run migrations/init_db.py
3. Set up regular backups
4. Enable SSL connections

## 🛡️ Security Considerations

- Change default admin password
- Use strong SECRET_KEY in production
- Enable HTTPS
- Implement rate limiting
- Set up database backups
- Monitor admin actions
- Regular security audits
- Keep dependencies updated

## 🐛 Troubleshooting

### Backend Issues
- **Database connection failed:** Check DATABASE_URL and PostgreSQL service
- **Import errors:** Ensure virtual environment is activated
- **Port already in use:** Change port in run.py

### Frontend Issues
- **Cannot connect to API:** Verify backend is running and API_BASE_URL is correct
- **Build errors:** Delete node_modules and reinstall
- **CORS errors:** Check CORS_ORIGINS in backend .env

### Database Issues
- **Tables not created:** Run init_db.py
- **Authentication failed:** Check PostgreSQL credentials
- **Enum errors:** Run the DDL script directly in psql

## 📝 License

MIT License - Feel free to use this project for learning or commercial purposes.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the README files in backend/ and frontend/
3. Check API documentation at /docs

## 🎓 Learning Resources

This project demonstrates:
- RESTful API design
- JWT authentication
- Role-based access control
- React component architecture
- State management with Context API
- Form validation
- Error handling
- Database design
- Transaction management
- Security best practices

## ⭐ Features Implemented

✅ User authentication and authorization
✅ Account management
✅ Money transfers with transaction tracking
✅ Bill payment system
✅ Transaction history with filters
✅ Admin dashboard with analytics
✅ User management (admin)
✅ Responsive design
✅ Data visualization with charts
✅ Password change functionality
✅ Profile management
✅ Transaction monitoring
✅ Admin action logging
✅ Role-based routing
✅ Error handling and validation
✅ Loading states
✅ Success/error alerts

## 🚀 Future Enhancements

Potential features to add:
- Email notifications
- Two-factor authentication
- Transaction export (PDF, CSV)
- Account statements
- Loan management
- Credit card integration
- Mobile app
- Real-time notifications
- Scheduled payments
- Multi-currency support
- Transaction categories
- Budget tracking
- Investment accounts

---

**Built with ❤️ using React and FastAPI**

