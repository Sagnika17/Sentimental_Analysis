Sentiment Analyis using news API
////////////////////////////////

1)Import Libraries:

import requests
from textblob import TextBlob
import smtplib
from email.mime.text import MIMEText

*requests: Used for making HTTP get and post requests to external APIs.
*TextBlob: A natural language processing library that can be used for processing textual data, including sentiment analysis.
*smtplib: Part of the Python standard library, it provides an interface for sending emails using the Simple Mail Transfer Protocol (SMTP).
*MIMEText: Part of the email module, it's used to create an email message with plain text content.

2)Class Definition:

class SentimentAnalysis:
    def __init__(self):
        # Replace the following with your email configuration
        self.sender_email = 'iamsagnikabhat@gmail.com'
        self.receiver_email = 'recipient_email@gmail.com'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.smtp_username = 'iamsagnikabhat@gmail.com'
        self.smtp_password = 'tfrb uxwt hopr lvpf'


*SentimentAnalysis: Defines a class that encapsulates methods and attributes related to sentiment analysis.
*Constructor (__init__ method):
*Initializes instance variables with email configuration details.

3)Method DownloadData:

def DownloadData(self):
    # Replace 'YOUR_API_KEY' with your actual News API key
    search_query = input("Enter the search query: ")
    api_key = '46671a0e40b7408ab0d020e3e9528b2f'
    url = f'https://newsapi.org/v2/everything?q={search_query}&apiKey={api_key}'
    result = requests.get(url)
    data = result.json()

*Takes user input for a search query.
*Constructs a URL with the News API key and the search query.
*Makes an HTTP GET request to the News API and converts the response to JSON.

4)Sentiment Analysis Loop:

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


*Iterates through the articles in the response.
*Checks if each article has content.
*Calls the analyze_sentiment method to get the sentiment score.
*Updates sentiment statistics and reasons lists based on the sentiment score.

5)Print Results:

        print(f"Sentiment Score  : {total_sentiment/num_articles}")
        if self.should_alert_user(total_sentiment/num_articles):
            self.send_email_alert(total_sentiment/num_articles)

        print("\nTop 5 Reasons for Positive Sentiment:")
        self.print_top_reasons(positive_reasons)

        print("\nTop 5 Reasons for Negative Sentiment:")
        self.print_top_reasons(negative_reasons)

*Prints the total sentiment score.
*Calls the should_alert_user method and sends an email alert if the condition is met.
*Prints the top 5 reasons for positive and negative sentiment.

6)analyze_sentiment method:

def analyze_sentiment(self, text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity
def analyze_sentiment(self, text):

*This line defines a method named analyze_sentiment that takes two parameters: self (a reference to the instance of the class) and text (the text for which sentiment analysis needs to be performed).
analysis = TextBlob(text)

*Here, a TextBlob object is created using the provided text. TextBlob is a part of the TextBlob library, and it provides a simple API for common natural language processing (NLP) tasks, including sentiment analysis.
return analysis.sentiment.polarity

*The sentiment analysis is performed using the TextBlob object's sentiment attribute, which returns a named tuple containing two properties: polarity and subjectivity. In this case, only polarity is used.
polarity is a float value ranging from -1 to 1, where:
Negative values indicate negative sentiment.
Positive values indicate positive sentiment.
0 indicates neutral sentiment.
The method returns the polarity value as the result of the sentiment analysis.

7)Alert Condition (should_alert_user method):

def should_alert_user(self, sentiment_score_threshold):
    # You can set your own threshold for when to send an alert
    return sentiment_score_threshold < -0.5

*Defines a condition to trigger an alert based on the sentiment score.
*Returns True if the sentiment score is below a threshold, otherwise False.

8)Email Alert Method (send_email_alert):

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

*Composes an email message with a subject and body.
*Uses the smtplib library to send the email through the SMTP server.

9)Print Top Reasons Method (print_top_reasons):

def print_top_reasons(self, reasons):
    reasons.sort(key=lambda x: abs(x[1]))
    for i in range(5):
        print("reason", i + 1, "-->")
        print(reasons.pop())

*Sorts the reasons list based on the absolute value of sentiment scores.
*Prints the top 5 reasons.

/////////////////////////////////////////////////////////////////////////////////////////////////////
 Now i shall discuss the sentiment analysis loop in detail:

total_sentiment = 0 (stores total sentiment score)
num_articles = 0    (stores total no. of articles)
positive_count = 0  (stores no. of positive sentiments)
negative_count = 0  (stores no. of negative sentiments) 
neutral_count = 0   (stores no. of neutral sentiments) 
positive_reasons = [](stores list of reasons for positive sentiments)
negative_reasons = [](stores list of reasons for negaitive sentiments)

if 'articles' in data:
(Checks if the key 'articles' exists in the data dictionary. This is a precautionary step to make sure there are articles in the response.)
    articles = data['articles']
    for article in articles:
(If there are articles, it retrieves the list of articles and iterates through each article in the list.)
        if 'content' in article:
(For each article, it checks if there is a 'content' key in the article dictionary. This is to ensure that the article has content to analyzed.)
            article_content = article['content']
            sentiment_score = self.analyze_sentiment(article_content)
            total_sentiment += sentiment_score
            num_articles += 1
(If there is content, it retrieves the content and calculates the sentiment score using the analyze_sentiment method. The sentiment score is then added to the total_sentiment and the num_articles counter is incremented.)
            if sentiment_score > 0:
                positive_count += 1
                positive_reasons.append((article_content, sentiment_score))
            elif sentiment_score < 0:
                negative_count += 1
                negative_reasons.append((article_content, sentiment_score))
            else:
                neutral_count += 1
(Based on the sentiment score, it increments the respective counters (positive_count, negative_count, or neutral_count) and appends a tuple of (article_content, sentiment_score) to the appropriate list (positive_reasons or negative_reasons.)

