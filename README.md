# SmartForce - Optimized Workout Training App

A high-performance, production-ready workout training application built with FastAPI, featuring comprehensive optimizations for scalability, security, and user experience.

## 🚀 Key Optimizations Implemented

### Performance Optimizations
- **Async Database Operations**: Implemented async SQLAlchemy for better concurrency
- **Redis Caching**: Intelligent caching for frequently accessed data
- **Connection Pooling**: Optimized database connection management
- **Gzip Compression**: Reduced response sizes for better network performance
- **Rate Limiting**: Protected against abuse with configurable limits

### Security Enhancements
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Security Headers**: Comprehensive security headers middleware
- **Input Validation**: Pydantic models for robust data validation
- **CORS Configuration**: Proper cross-origin resource sharing setup

### Monitoring & Observability
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **Prometheus Metrics**: Request counts, latency, and custom metrics
- **Health Checks**: Application and database health monitoring
- **Request Tracking**: Full request/response logging with performance metrics

### Production Readiness
- **Docker Multi-stage Build**: Optimized container images
- **Database Migrations**: Alembic for schema version control
- **Environment Configuration**: Centralized settings management
- **Error Handling**: Comprehensive error handling and recovery

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │   FastAPI App   │    │   PostgreSQL    │
│   (Load Bal.)   │◄──►│   (API Server)  │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Redis Cache   │    │   Prometheus    │    │   Grafana       │
│   (Session/Data)│    │   (Monitoring)  │    │   (Dashboard)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

- **Backend**: FastAPI 0.104.1
- **Database**: PostgreSQL 15 + SQLAlchemy 2.0
- **Cache**: Redis 7
- **Authentication**: JWT + Passlib
- **Monitoring**: Prometheus + Grafana
- **Containerization**: Docker + Docker Compose
- **Logging**: Structlog
- **Testing**: Pytest

## 📦 Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Git

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend-python
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application stack**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Grafana: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090

### Local Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export DATABASE_URL="sqlite:///./smart_force.db"
   export SECRET_KEY="your-secret-key"
   export DEBUG=true
   ```

4. **Initialize database**
   ```bash
   alembic upgrade head
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./smart_force.db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `REDIS_URL` | Redis connection string | `None` |
| `ENVIRONMENT` | Environment (dev/prod) | `development` |
| `DEBUG` | Debug mode | `False` |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | `60` |

### Database Configuration

The application supports both SQLite (development) and PostgreSQL (production):

```bash
# Development
DATABASE_URL=sqlite:///./smart_force.db

# Production
DATABASE_URL=postgresql://user:password@localhost/smartforce_db
```

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh token

### Training Management
- `GET /api/v1/trainings/{id}` - Get training by ID
- `POST /api/v1/trainings/` - Create new training
- `PUT /api/v1/trainings/{id}` - Update training
- `DELETE /api/v1/trainings/{id}` - Delete training
- `GET /api/v1/users/{id}/trainings` - Get user trainings
- `GET /api/v1/professors/{id}/trainings` - Get professor trainings

### Monitoring
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

## 🔍 Monitoring & Logging

### Logs
Application logs are structured and include:
- Request correlation IDs
- Performance metrics
- Error tracking
- User activity

### Metrics
Prometheus metrics include:
- HTTP request counts
- Response latency
- Error rates
- Cache hit/miss ratios

### Dashboards
Grafana dashboards provide:
- Real-time application metrics
- Database performance
- User activity analytics
- Error rate monitoring

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_training.py
```

## 🚀 Deployment

### Production Deployment

1. **Update environment variables**
   ```bash
   export ENVIRONMENT=production
   export DATABASE_URL=postgresql://...
   export SECRET_KEY=your-secure-secret-key
   ```

2. **Build and deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Run database migrations**
   ```bash
   docker-compose exec app alembic upgrade head
   ```

### Scaling

The application is designed to scale horizontally:

```bash
# Scale the application
docker-compose up -d --scale app=3

# Use a load balancer (nginx) for distribution
```

## 🔒 Security Features

- **Authentication**: JWT-based authentication with refresh tokens
- **Authorization**: Role-based access control
- **Input Validation**: Comprehensive data validation
- **Rate Limiting**: Protection against abuse
- **Security Headers**: XSS, CSRF, and other security protections
- **Password Security**: Bcrypt hashing with salt

## 📈 Performance Optimizations

### Caching Strategy
- **User Data**: 1 hour cache
- **Training Data**: 30 minutes cache
- **Exercise Data**: 2 hours cache
- **API Responses**: Intelligent cache invalidation

### Database Optimizations
- **Connection Pooling**: 20 connections with 30 overflow
- **Query Optimization**: Indexed foreign keys
- **Async Operations**: Non-blocking database calls

### API Optimizations
- **Pagination**: Efficient data retrieval
- **Compression**: Gzip compression for responses
- **Rate Limiting**: Configurable per-endpoint limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation at `/docs`
- Review the health endpoint at `/health`

## 🔄 Changelog

### v1.0.0 - Initial Release
- Complete workout training application
- JWT authentication
- Redis caching
- Prometheus monitoring
- Docker deployment
- Comprehensive API documentation 