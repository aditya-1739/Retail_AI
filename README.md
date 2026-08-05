# Retail AI

Retail AI is an end-to-end, containerized smart retail management and customer engagement solution. The platform integrates a modern React frontend dashboard with a high-performance FastAPI backend. It leverages multiple machine learning models—powered by TensorFlow and Scikit-Learn—to deliver smart features such as automated product classification, facial customer recognition, customer review sentiment analysis, and an interactive shopping assistant chatbot.

---

## Features

- **Product Classification**: Classifies uploaded clothing or product images into Fashion-MNIST categories (T-shirt, Trouser, Pullover, Dress, etc.) using a pre-trained CNN (MobileNetV2) running in a non-blocking threadpool.
- **Customer Face Recognition**: Identifies registered customers from captured photos or webcam streams using a pre-trained classification model.
- **Sentiment Analysis**: Evaluates customer reviews as Positive or Negative using a TF-IDF vectorizer and a machine learning classifier.
- **Interactive Chatbot**: Engages users with an AI shopping assistant powered by an intent classification model and a retail intents database.
- **User Authentication**: Secure JWT-based registration, login, and authorization (User/Admin roles) to protect endpoints and audit client access.
- **Access Logging & Auditing**: Backend middleware automatically logs prediction queries and API metadata into the SQLite database for reporting.

---

## Tech Stack

### Frontend
- **React** (JavaScript library for building user interfaces)
- **Vite** (Next-generation frontend tooling)
- **Bootstrap** (For sleek, responsive layouts)

### Backend
- **FastAPI** (High-performance modern Python web framework)
- **Uvicorn** (Lightning-fast ASGI server implementation)
- **SQLAlchemy** (SQL toolkit and Object-Relational Mapper)

### AI & Machine Learning
- **TensorFlow** (For deep learning-based image classification)
- **Scikit-learn** (For NLP sentiment analysis, face classification, and chatbot intent matching)
- **OpenCV** (Pre-trained computer vision pipeline requirements)

### Database
- **SQLite** (Default lightweight, serverless relational database)

### Deployment & DevOps
- **Docker** (Containerization of backend and frontend microservices)
- **Docker Compose** (Multi-container orchestration)

---

## Project Structure

```text
Retail_AI/
├── SmartRetailAI/             # ML notebooks, datasets, and scripts for model training
├── smart-retail-ai-backend/   # FastAPI REST API Backend
│   ├── app/
│   │   ├── core/              # App configurations, secrets, and JWT security utilities
│   │   ├── db/                # SQLAlchemy database schema and session handlers
│   │   ├── models/            # Pre-trained ML weights (.h5, .pkl) and intents JSON
│   │   ├── routers/           # Modular route groups (auth, chatbot, face, product, sentiment)
│   │   └── services/          # Model loaders and inference helper functions
│   ├── tests/                 # Unit tests built with pytest
│   ├── Dockerfile             # Container configuration for Python 3.12-slim
│   ├── requirements.txt       # Backend Python dependencies (fixed & verified)
│   └── .env.example           # Backend environment variable template
├── smart-retail-frontend/     # React & Vite Frontend Dashboard
│   ├── src/
│   │   ├── components/        # Interactive widgets for each AI module
│   │   ├── pages/             # Landing page template
│   │   └── services/          # API integrations with Axios clients
│   ├── Dockerfile             # Frontend container config (multistage Node build)
│   └── .env.example           # Frontend environment variable template
└── docker-compose.yml         # Shared network container orchestration script
```

---

## Installation

### Clone

```bash
git clone https://github.com/aditya-1739/Retail_AI.git
cd Retail_AI
```

### Run using Docker Compose (Recommended)

1. Make sure you have **Docker** and **Docker Compose** installed on your system.
2. Build and start the services:
   ```bash
   docker compose up --build -d
   ```
3. Access the applications:
   - **Frontend UI**: [http://localhost:5173](http://localhost:5173)
   - **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
   - **Backend Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

### Local Manual Installation (Development)

If you prefer to run the services outside Docker, follow these steps:

#### Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd smart-retail-ai-backend
   ```
2. Initialize and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup
1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd smart-retail-frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```
