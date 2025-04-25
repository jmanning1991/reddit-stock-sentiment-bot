# === Standard Library ===
import os  # For environment variable access
from dotenv import load_dotenv  # For loading local .env files
import threading  # To run multiple subreddit monitors concurrently
import traceback  # For detailed exception tracebacks in logs
import smtplib  # For sending email notifications
import ssl  # For securing SMTP connection
from datetime import datetime, timedelta  # For timestamp comparisons
from email.message import EmailMessage  # For constructing email content
import json  # For handling API keys and structured config data

# 🔑 Load .env variables before any imports that rely on them
load_dotenv()

# === Third-Party Libraries ===
import openai  # OpenAI API for sentiment analysis
import praw  # Reddit API wrapper
import pandas as pd  # Data handling (optional for future expansion)
import yfinance as yf  # For pulling stock price data
import gspread  # Google Sheets integration
from flask import Flask  # Web app framework for Azure ping/healthcheck
from google.oauth2.service_account import Credentials  # Auth for Sheets API

# === Internal Modules ===
from config import subreddits, ticker_keywords, EMAIL_LIST  # Local config
import functions as f  # Core logic for subreddit monitoring, alerts, etc.





app = Flask(__name__)

@app.route("/")
def healthcheck():
    return "Bot is running!"

def run_bot():

    
    
    reddit = praw.Reddit(
        client_id = os.getenv("REDDIT_CLIENT_ID"),
        client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent = os.getenv("REDDIT_USER_AGENT"),
    )
    openai_api_key = os.getenv("OPENAI_API_KEY") #set openai api_key
    openai_client = openai.OpenAI(api_key=openai_api_key)  # Initialize OpenAI client
    email_list = EMAIL_LIST # Email list
    email_password = os.getenv("GOOGLE_APP_PASS") # Main gmail app pass
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets", 
              "https://www.googleapis.com/auth/drive"]
    
    if os.getenv("GOOGLE_CREDS_JSON"):
        creds_json = os.getenv("GOOGLE_CREDS_JSON")
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    else:
        google_creds_path = os.getenv("GOOGLE_CREDS_PATH", "./GoogleAPI.json")
        creds = Credentials.from_service_account_file(google_creds_path, scopes=scopes)

    
    google_sheets_client = gspread.authorize(creds)
    # Open Google Sheet
    sheet = google_sheets_client.open("RedditBotLogs").sheet1  # Adjust for multiple sheets
    # Append data
    data = ["Timestamp", "Ticker", "Title", "Sentiment", "Yesterday Close", "Current Price", "Percent Change", "URL"]
    
    
    # Create a list to store threads
    threads = []
    print("Starting bot...")
    
    # Start a thread for each subreddit
    for sub in subreddits:
        thread = threading.Thread(
            target=f.monitor_subreddit,
                args=(
                    sub,
                    ticker_keywords,
                    reddit,
                    sheet,              # ✅ Google Sheets object
                    openai_client,      # ✅ Initialized OpenAI client instance
                    email_list,
                    email_password
            )
        )
        thread.daemon = True  # Ensures the thread shuts down if the main program exits
        thread.start()
        threads.append(thread)
    
    # Keep the main script alive
    for thread in threads:
        thread.join()



if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    print("Flask server started.")
    app.run(host="0.0.0.0", port=5000)

