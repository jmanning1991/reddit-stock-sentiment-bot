# === Standard Library ===
import traceback
from datetime import datetime
import smtplib
import ssl
import textwrap
from email.message import EmailMessage

# === Third-Party ===
import yfinance as yf





def log_to_sheets(sheet, timestamp, ticker, company_name, title, sentiment, yesterday_close, current_price, percent_change, url):
    data = [timestamp, ticker, company_name, title, sentiment, yesterday_close, current_price, percent_change, url]
    sheet.append_row(data)





def ticker_info(ticker):
    ticker_obj = yf.Ticker(ticker)
    
    # Get yesterday's close price
    history = ticker_obj.history(period="2d")  # Get last 2 days to extract yesterday's close
    yesterday_close = history['Close'].iloc[0] if len(history) > 1 else None  # First row is yesterday's close
    
    # Get live price
    current_price = ticker_obj.info.get("regularMarketPrice", None)  # Real-time market price
    
    # Get company name
    company_name = ticker_obj.info.get("longName", ticker)  # Default to ticker if name missing

    # Calculate percentage change
    if yesterday_close and current_price:
        percent_change = ((current_price - yesterday_close) / yesterday_close) * 100
    else:
        percent_change = None

    return company_name, current_price, yesterday_close, percent_change




def analyze_sentiment(title, body, client):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Classify this post as Positive, Negative, or Neutral."},
                {"role": "user", "content": f"Title: {title}\n\nBody: {body}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API Error for post '{title}': {e}")
        return None


def gmail_sender(subject, body, recipient_list, app_password):
    EMAIL_ADDRESS = "josephmichaelmanning@gmail.com"
    EMAIL_PASSWORD = app_password  # 16-character App Password

    # ✅ Create the email message
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(recipient_list)  # Correct variable name
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")






def monitor_subreddit(sub, ticker_keywords, reddit, sheet, openai_client, email_list, email_password):
    """Monitors a single subreddit stream for relevant posts."""
    
    try:
        subreddit = reddit.subreddit(sub)
        for submission in subreddit.stream.submissions(skip_existing=True):
            reddit_title = submission.title
            reddit_body = submission.selftext
            post_url = submission.url  # Capture the Reddit post URL

            for ticker, keywords in ticker_keywords.items():
                if any(keyword.lower() in reddit_title.lower() for keyword in keywords):
                    print(f"[INFO] New post found: {reddit_title} in r/{submission.subreddit} (Matched: {ticker})")

                    # Gather Yahoo Finance Data
                    company_name, current_price, yesterday_close, percent_change = ticker_info(ticker)

                    # Perform Sentiment Analysis
                    sentiment = analyze_sentiment(reddit_title, reddit_body, openai_client)

                    print(f"[INFO] Sentiment: {sentiment}")  # Debugging output

                    if sentiment.lower() != "neutral":
                        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log_to_sheets(
                            sheet,
                            formatted_time, ticker, company_name, reddit_title,
                            sentiment, yesterday_close, current_price, percent_change, post_url
                        )
                        print(f"Information for {ticker} has been logged to Google Sheets!")
                    
                        # ✅ Send email alert
                        email_subject = f"[{sentiment}] {ticker} mentioned in r/{submission.subreddit}"
                        email_body = textwrap.dedent(f"""
                            Title: {reddit_title}
                            Ticker: {ticker}
                            Sentiment: {sentiment}
                            Price: {current_price:.2f} (Prev Close: {yesterday_close:.2f}, Δ: {percent_change:.2f}%)

                            Link: {post_url}
                        """).strip()
                        print(f"[DEBUG] Sending email to: {email_list} | Subject: {email_subject}")
                        gmail_sender(email_subject, email_body, email_list, email_password)

    except Exception as e:
        print(f"[ERROR] Exception in subreddit monitoring ({sub}): {e}")
        traceback.print_exc()
