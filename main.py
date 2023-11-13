import requests
from textblob import TextBlob
import re
import  nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


nltk.download('stopwords')
nltk.download('punkt')
class SentimentAnalysis:

    def DownloadData(self, search_query):
        # Replace 'YOUR_API_KEY' with your actual News API key
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
                        positive_reasons.extend(self.get_top_reasons(article_content))
                    elif sentiment_score < 0:
                        negative_count += 1
                        negative_reasons.extend(self.get_top_reasons(article_content))
                    else:
                        neutral_count += 1

                    print(f"Sentiment Score for '{article['title']}': {sentiment_score}")

        if num_articles > 0:
            average_sentiment = total_sentiment / num_articles
            print(f"\nAverage Sentiment Score for all articles: {average_sentiment:.4f}")
            print(f"Positive Articles: {positive_count}")
            print(f"Negative Articles: {negative_count}")
            print(f"Neutral Articles: {neutral_count}")

            print("\nTop 5 Reasons for Positive Sentiment:")
            self.print_top_reasons(positive_reasons)

            print("\nTop 5 Reasons for Negative Sentiment:")
            self.print_top_reasons(negative_reasons)

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity

    def get_top_reasons(self, text):
        # Add your logic to extract and analyze the reasons for sentiment
        # For simplicity, this function returns a list of words in the text.
        text = re.sub(r'[^A-Za-z]', ' ', text.lower())

        # Tokenize the text
        words = word_tokenize(text)

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]

        return words

    def print_top_reasons(self, reasons):
        from collections import Counter
        reasons_counter = Counter(reasons)
        for reason, count in reasons_counter.most_common(5):
            print(f"{reason}: {count}")

if __name__ == "__main__":
    search_query = input("Enter the search query: ")
    sa = SentimentAnalysis()
    sa.DownloadData(search_query)
