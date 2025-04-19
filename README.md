
# 📈 Reddit Stock Sentiment Bot

This project monitors Reddit posts across financial subreddits, analyzes sentiment using GPT, logs relevant matches to Google Sheets, and sends real-time email alerts for actionable mentions. 

It’s a full-stack Python automation pipeline built with modular design and multi-threaded monitoring.

---

## 🧠 Features

- **Subreddit Monitoring** — Streams live posts from finance-related subreddits
- **AI Sentiment Analysis** — Classifies post tone using OpenAI's GPT-3.5
- **Yahoo Finance Enrichment** — Fetches live price, company info, and price change
- **Google Sheets Logging** — Logs results in real-time for visibility and tracking
- **Gmail Alerts** — Sends sentiment-based email alerts for matched tickers
- **Multi-threaded Execution** — Efficiently handles multiple subreddits in parallel

---

## 🚀 Setup Instructions

### 1. **Clone the Repo**
```bash
git clone https://github.com/your-username/reddit-stock-sentiment-bot.git
cd reddit-stock-sentiment-bot
```

### 2. **Create and Activate a Virtual Environment**
```bash
conda create --name redditbot python=3.11
conda activate redditbot
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Create Your `.env` File**
Create a `.env` file in the root directory with the following variables:
```env
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=your_custom_user_agent

OPENAI_API_KEY=your_openai_api_key
GOOGLE_APP_PASS=your_16_char_google_app_password
GOOGLE_CREDS_PATH=./GoogleAPI.json
```

> 📌 **Note:** Your `GoogleAPI.json` file (Google Sheets service credentials) must be placed in the root folder.

---

## 🧪 Running the Bot

### Option 1: Run via Python
```bash
python main.py
```

### Option 2: Run in Jupyter Notebook
You can also run the `main.py` logic in a `.ipynb` format if you want more step-by-step visibility.

---

## 🗂 Folder Structure

```
reddit-stock-sentiment-bot/
├── main.py
├── functions.py
├── config.py
├── .env
├── .env.example
├── requirements.txt
├── GoogleAPI.json          # (excluded from GitHub via .gitignore)
├── .gitignore
├── LICENSE
└── README.md
```

> 📌 Note: `.env` and `GoogleAPI.json` are excluded from the GitHub repo but are required to run the bot locally.

---

## 🧼 Sample Output

- **Email Alert**
  ```
  Subject: [Positive] NVDA mentioned in r/wallstreetbets
  Body:
  Title: Nvidia earnings blow past expectations!
  Sentiment: Positive
  Price: $789.45 (Prev Close: $774.00, Δ: +1.99%)
  ```

- **Google Sheet Row**
  ```
  Timestamp | Ticker | Title | Sentiment | Close | Current | Δ% | URL
  ```

---

## ⚠️ Trigger Word Disclaimer

This bot uses a static dictionary of trigger keywords mapped to stock tickers (e.g., “Tesla” → TSLA, “Elon” → TSLA). While this approach works well in many cases, it is not foolproof:

- A post may mention a trigger word in a different context (e.g., “Elon” in a post about Twitter).
- Multiple tickers may be matched for a single post if their keywords overlap.
- The bot does not yet account for sentiment **per ticker** if multiple are mentioned.

This is expected behavior for a lightweight proof of concept and can be improved with more advanced NLP techniques (e.g., named entity recognition, co-reference resolution, etc).

> 📌 Bottom line: It’s a smart, fast scanner — but not a financial oracle.

---

## 💬 Acknowledgements

Special thanks to **Mike Knoll** for inspiring the development of this bot. His input helped shape the foundation of the idea.

---

## 🔒 .gitignore Reminder

Your `.gitignore` should at least include:
```
.env
GoogleAPI.json
__pycache__/
```

---

## 🎯 Author

**Joseph Manning** — Business Intelligence Architect | AI Automation Enthusiast  
[LinkedIn](https://www.linkedin.com/in/joseph-manning-4a67256a/)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
