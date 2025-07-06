# AI Fitness Planner Backend

AI Fitness Planner is a backend system built with FastAPI, PostgreSQL, and Groq AI integration. It provides diet and workout recommendations based on user input and authenticates users securely with JWT tokens.


---


## 🚀 Features

* User registration and login with JWT authentication
* Generate personalized diet plans using Groq AI
* Generate workout routines based on fitness level and goals
* PostgreSQL database integration via SQLAlchemy
* Structured, scalable FastAPI application layout


---


## 📂 Project Structure


```
ai_fitness_planner/
├── backend/
│   └── app/
│       ├── api/v1/              # Versioned API routes
│       ├── core/                # Config and security logic
│       ├── db/                  # DB session and initialization
│       ├── models/              # SQLAlchemy models
│       ├── schemas/             # Pydantic schemas
│       ├── services/            # Groq, auth helpers
│       ├── utils/               # Logging and response utilities
│       └── main.py              # FastAPI entrypoint
├── frontend/                   # (To be added)
├── .env                        # Environment configuration
├── requirements.txt            # Python dependencies
├── uv.lock / pyproject.toml    # uv package manager files
```

---

## 📃 Environment Variables

Create a `.env` file in the root directory:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/ai_fitness_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## ⚙️ Installation

### 1. Install Dependencies

```bash
uv sync
```

### 2. Run the App

```bash
uvicorn app.main:app --reload --app-dir backend
```

### 3. Access Docs

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🦄 Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Groq AI
* JWT (via `python-jose`)
* uv (as Python package manager)

---

