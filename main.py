import requests
from textblob import TextBlob
import smtplib
from email.mime.text import MIMEText


class SentimentAnalysis:
    def __init__(self):
        # Replace the following with your email configuration
        self.sender_email = 'iamsagnikabhat@gmail.com'
        self.receiver_email = 'recipient@gmail.com'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.smtp_username = 'iamsagnikabhat@gmail.com'
        self.smtp_password = 'tfrb uxwt hopr lvpf'

    def DownloadData(self):
        # Replace 'YOUR_API_KEY' with your actual News API key
        search_query = input("Enter the search query: ")
        api_key = '46671a0e40b7408ab0d020e3e9528b2f'
        url = f'https://newsapi.org/v2/everything?q={search_query}&apiKey={api_key}'
        result = requests.get(url)
        data = result.json()

        total_sentiment = 0
        num_articles = 0
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        positive_reasons = []
        negative_reasons = []

        if 'articles' in data:
            articles = data['articles']
            for article in articles:
                if 'content' in article:
                    article_content = article['content']
                    sentiment_score = self.analyze_sentiment(article_content)
                    total_sentiment += sentiment_score
                    num_articles += 1

                    if sentiment_score > 0:
                        positive_count += 1
                        positive_reasons.append((article_content, sentiment_score))
                    elif sentiment_score < 0:
                        negative_count += 1
                        negative_reasons.append((article_content, sentiment_score))
                    else:
                        neutral_count += 1

            print(f"Sentiment Score  : {total_sentiment}")
            if self.should_alert_user(total_sentiment):
                self.send_email_alert(total_sentiment)

            print("\nTop 5 Reasons for Positive Sentiment:")
            self.print_top_reasons(positive_reasons)

            print("\nTop 5 Reasons for Negative Sentiment:")
            self.print_top_reasons(negative_reasons)

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity

    def should_alert_user(self, sentiment_score_threshold):
        # You can set your own threshold for when to send an alert
        return sentiment_score_threshold < -0.5

    def send_email_alert(self, sentiment_score):
        subject = 'Sentiment Alert'
        body = f'The sentiment score has dropped to {sentiment_score}. You might want to check it.'

        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = self.sender_email
        message['To'] = self.receiver_email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.sender_email, [self.receiver_email], message.as_string())

    def print_top_reasons(self, reasons):
        reasons.sort(key=lambda x: abs(x[1]))
        for i in range(5):
            print("reason", i + 1, "-->")
            print(reasons.pop())


if __name__ == "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
