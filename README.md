# Reddit Sentiment Bot

A sentiment analysis bot that monitors new posts across multiple subreddits for stock-related tickers, scores sentiment using GPT, and logs the results to a Google Sheet.

---

## ⚙️ Features

- **Multi-threaded Monitoring** — Each subreddit runs in its own thread for parallel listening
- **Ticker Keyword Matching** — Only responds to posts that mention tickers from a configurable list
- **OpenAI Sentiment Analysis** — Uses GPT API to classify tone as Positive, Negative, or Neutral
- **Google Sheets Logging** — Logs every match with full metadata to a connected spreadsheet
- **Email Notifications** — Optionally send an email with the analysis summary
- **CI/CD Deployment** — GitHub Actions builds and deploys to Azure with Docker Hub integration
- **Cloud-Ready Containerization** — Deployable as a headless or HTTP-backed service

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/jmanning1991/reddit-stock-sentiment-bot.git
cd reddit-stock-sentiment-bot
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your environment variables
Create a `.env` file with your credentials:

```env
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_agent
GOOGLE_APP_PASS=your_google_app_password
OPENAI_API_KEY=your_openai_key
GOOGLE_CREDS_PATH=./GoogleAPI.json
```

### 5. [Optional] Add Flask for Azure Deployment
If you're deploying to Azure App Service (container-based), Flask is used to serve a basic healthcheck route so the container stays alive:
```bash
pip install flask
```
This is already included in `requirements.txt`, but important to know **why it's there**.

---

## 🧪 Running the Bot

### Option 1: Run via Terminal
```bash
python main.py
```

### Option 2: Run via IDE
Just run `main.py` directly inside your IDE of choice.

### Option 3: Run in Azure via Docker + GitHub Actions
This project includes a full CI/CD pipeline:

- Push to `main` → GitHub builds the Docker image
- Image is pushed to Docker Hub
- Azure App Service pulls and deploys it
- The container serves a lightweight Flask route on port `5000` to pass Azure’s health checks
- The sentiment bot runs in the background via multithreading

> ⚠️ Azure requires an HTTP server on port `5000` to validate container health. A minimal Flask app is included in `main.py` for this purpose.

---

## 🔁 CI/CD Pipeline Overview

This project uses GitHub Actions to deploy the latest version of the bot automatically:

- **GitHub Actions Workflow (`.github/workflows/deploy.yml`)**
  - Builds a Docker image from your source
  - Logs into Docker Hub and pushes the image
  - Logs into Azure using a secure service principal
  - Tells Azure to redeploy using the latest image

- **Docker Hub**
  - Hosts the public `jmanning1991/reddit-sentiment-bot:latest` container

- **Azure App Service (Linux)**
  - Configured to pull from Docker Hub
  - Expects an HTTP response on port `5000`
  - Flask's healthcheck enables long-term container uptime

> You can find this entire pipeline documented in the GitHub repo under `.github/workflows/`

---

## 📁 .gitignore Reminder
Your `.env`, Google credentials, and sensitive keys should never be committed.

---

> ✅ Built with 💻 GitHub Actions, 🐋 Docker, and ☁️ Azure App Service

