# === Standard Library ===
import os
import threading
import traceback
import smtplib
import ssl
from datetime import datetime, timedelta
from email.message import EmailMessage
import json

# === Third-Party Libraries ===
import openai
import praw
import pandas as pd
import yfinance as yf
import gspread
from flask import Flask
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# === Internal Modules ===
from config import subreddits, ticker_keywords
import functions as f




app = Flask(__name__)

@app.route("/")
def healthcheck():
    return "Bot is running!"

def run_bot():

    
    
    load_dotenv()
    reddit = praw.Reddit(
        client_id = os.getenv("REDDIT_CLIENT_ID"),
        client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent = os.getenv("REDDIT_USER_AGENT"),
    )
    openai_api_key = os.getenv("OPENAI_API_KEY") #set openai api_key
    openai_client = openai.OpenAI(api_key=openai_api_key)  # Initialize OpenAI client
    email_list = ["josephmichaelmanning@gmail.com"] # Email list
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

