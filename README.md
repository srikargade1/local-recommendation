# 🗺️ Local Recommendations App

A full-stack web application that provides personalized local recommendations using the Foursquare API. Built with a Flask backend and React frontend, containerized using Docker, and deployed via Render with CI/CD automation using GitHub Actions.

## 🚀 Live Demo

- **Frontend:** [https://frontend-xxxxx.onrender.com](https://frontend-xxxxx.onrender.com)
- **Backend:** [https://backend-xxxxx.onrender.com](https://backend-xxxxx.onrender.com)

> Replace these with your actual Render URLs

---

## 📦 Tech Stack

| Layer      | Tech                                    |
|------------|------------------------------------------|
| Frontend   | React, JavaScript, Tailwind, Nginx       |
| Backend    | Flask, Gunicorn, Python, OpenAI, CORS    |
| API        | Foursquare Places API                    |
| DevOps     | Docker, Docker Compose, Render           |
| CI/CD      | GitHub Actions + Render Deploy Hooks     |

---

## ⚙️ Features

- 🌐 Full-stack deployment using Docker containers
- 📍 Location-based recommendations via Foursquare API
- 🤖 Smart ranking algorithm for better result ordering
- 🔐 Secure environment variable management
- 🚦 CI/CD pipeline using GitHub Actions
- 🧪 Separate staging and production environments

---

## 🧠 How It Works

1. **Frontend (React)**:  
   Calls the backend API to fetch place recommendations and displays results using a clean UI.

2. **Backend (Flask)**:  
   Processes user input, communicates with the Foursquare API, ranks results using a custom scoring algorithm, and returns relevant places.

3. **CI/CD Pipeline**:  
   - Push to `dev` → deploys to staging
   - Push to `main` → deploys to production

---

## 🛠️ Local Development

### 1. Clone the repo

```bash
git clone https://github.com/srikargade1/local-recommendation.git
cd local-recommendation
````

### 2. Create environment files

Create `.env` files inside `backend/` and `frontend/`:

#### `backend/.env`

```
OPENAI_API_KEY=your-key
FOURSQUARE_API_KEY=your-key
```

#### `frontend/.env`

```
REACT_APP_API_URL=http://localhost:5000
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

Frontend: `http://localhost:3000`
Backend: `http://localhost:5000`

---

## 🧪 Deployment

* Render handles backend and frontend separately
* GitHub Actions triggers deploys via deploy hooks on push
* `.github/workflows/deploy.yml` handles environment-based deployments

---

## 📁 Project Structure

```
local-recommendation/
│
├── backend/           # Flask backend
│   ├── app.py
│   ├── core/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/          # React frontend
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── render.yaml 
├── docker-compose.yml       # Render deployment config
└── .github/workflows/ # GitHub Actions CI/CD
```

---

## 🙏 Acknowledgements

* [Foursquare Places API](https://developer.foursquare.com/)
* [Render](https://render.com/)
* [OpenAI](https://openai.com/)
* [Docker](https://www.docker.com/)
* [GitHub Actions](https://github.com/features/actions)

---

## 📬 Contact

**Venkata Gade**
[LinkedIn](www.linkedin.com/in/gadevenkata)
[GitHub](https://github.com/srikargade1)
