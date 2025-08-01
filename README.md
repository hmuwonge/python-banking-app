# 🏦 SmartBank API
A fully featured, production-grade banking API built with **FastAPI**, containerized using **Docker**, and powered by **Celery**, **Redis**, and **RabbitMQ** for asynchronous processing. Integrated AI/ML modules enhance transaction analysis and fraud detection capabilities.
![img.png](img.png)


---

## 🚀 Features

- ✅ FastAPI-based RESTful banking endpoints
- 🔐 JWT Authentication & Role-based access control
- 💸 Transaction management (transfers, deposits, withdrawals)
- 📊 Account statements & analytics
- 🔁 Async task queues with Celery + RabbitMQ
- 🧠 AI/ML models for fraud detection & transaction classification
- 📦 Dockerized for full stack deployment
- 🔍 Audit trails & activity logs

---

## 🧰 Tech Stack

| Layer         | Technology        |
|---------------|-------------------|
| Backend API   | FastAPI           |
| Auth          | JWT / OAuth2      |
| Async Tasks   | Celery + RabbitMQ |
| Cache / Queue | Redis             |
| ML Models     | scikit-learn / XGBoost / PyTorch (customizable) |
| Deployment    | Docker / Docker Compose |

---

## 🏗️ Setup & Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/smartbank-api.git
   cd smartbank-api
   ```

2. **Environment variables**  
   Create a `.env` file:
   ```env
   DATABASE_URL=postgresql://user:password@db:5432/smartbank
   SECRET_KEY=your-secret-key
   REDIS_URL=redis://localhost:6379
   BROKER_URL=amqp://guest:guest@rabbitmq:5672//
   ```

3. **Build with Docker**  
   ```bash
   docker-compose up --build
   ```

---

## 📁 Key Modules

### 🔐 `auth`
- JWT auth implementation
- User roles: admin, customer, auditor

### 💸 `transactions`
- Transfer, deposit, withdraw
- Daily limits & approval workflows

### 📊 `analytics`
- Generate account reports
- Summarize activity trends

### 🧠 `ml`
- Fraud detection model
- Real-time inference via async tasks
- Transaction risk scoring

---

## 🧪 Testing

```bash
pytest --cov=.
```

Use mock transactions to test fraud detection pipeline and confirm classification accuracy.

---

## 🤖 ML Integration

- Pre-trained models can be swapped via configuration
- Model training pipeline included (with sample datasets)
- Threshold-based alerting for suspicious activity

---

## 📦 API Documentation

Accessible via Swagger UI:

```
http://localhost:8000/docs
```

Includes schema for all endpoints, auth flow, and sample payloads.

---

## 📈 Roadmap

- ✅ Multi-tenant support
- 🔜 KYC onboarding module
- 🔜 OpenBanking integration
- 🔜 Real-time transaction monitoring dashboards

---

## 👥 Contributors

- Muwonge Hassan — Founder & Lead Developer  
- Open to PRs and contributions. See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License © 2025 Muwonge Hassan | hassansaava@gmail.com

```

---
