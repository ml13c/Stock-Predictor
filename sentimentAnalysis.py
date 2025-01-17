from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from bs4 import BeautifulSoup
import requests

sia = SentimentIntensityAnalyzer()

# this will change into different urls but this is just a place holder for now
url = "https://www.investopedia.com/watch-these-intuitive-surgical-price-levels-stock-hits-another-record-high-8775500"

# REMEMBER TO USE VPN JUST IN CASE(to not get blocked)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

response = requests.get(url, headers=headers)

# this will vary from website to website since their 
# class names will be different so might have to train a model/find another way
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main body text of the article (yahoo finance example)
    btexts = soup.find_all("p")  # yahoo just uses p tags
    body_text = [text.get_text(strip=True) for text in btexts]

    # combine text 
    combined_text = " ".join(body_text)

    print("Extracted Text:", combined_text)
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    body_text = []

# Example list of text pieces
texts = body_text  # List of paragraphs extracted

# Analyze sentiment for each text
results = []
for text in texts:
    sentiment_score = sia.polarity_scores(text)  # get scores
    # set sentiment category(might have to change once I learn more about stocks)
    if sentiment_score['compound'] > 0.05:  # Positive threshold
        sentiment = 'positive'
    elif sentiment_score['compound'] < -0.05:  # Negative threshold
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    # Append the result
    results.append({'Text': text, 'Sentiment': sentiment})

# data frame 
df = pd.DataFrame(results)

# occurence count of each sentiment category
if not df.empty:
    sentiment_counts = df['Sentiment'].value_counts()
    print("Sentiment Counts:")
    print(sentiment_counts)

    # Optional: Display results for verification
    print("\nDetailed Results:")
    print(df)
else:
    print("No text was analyzed.")
