import sys
import pandas as pd
from requests_html import HTMLSession
import datetime
import re  # Import the regular expression module

# Set project path
path = '/Users/yashy/sudha project/'  # Update this to your actual path
sys.path.append(path)

# Initialize session
session = HTMLSession()

# Companies dictionary
companies = {
    "RI": "relianceindustries",
    "TCS": "tataconsultancyservices",
    "HDFCB": "hdfcbank",
    "BA": "bhartiairtel",
    "ICICI": "icicibank",
    "INFY": "infosys",
    "SBI": "statebankofindia",
    "HUL": "hindustanunilever",
    "BAJF": "bajajfinance",
    "ITC": "itc",
    "LIC": "lifeinsurancecorporation",
    "HCLT": "hcltechnologies",
    "LT": "larsentoubro",
    "SUNP": "sunpharmaindustries",
    "MSIL": "marutisuzuki",
    "KMB": "kotakmahindrabank",
    "M&M": "mahindraandmahindra",
    "UTCEM": "ultratechcement",
    "WIPRO": "wipro",
    "AXISB": "axisbank",
    "BAJFSV": "bajajfinserv",
    "NTPC": "ntpc",
    "ONGC": "ongc",
    "TITAN": "titancompany",
    "ADANIE": "adanienterprises"
}

# Initialize list to hold all data
all_news_data = []

# Loop through the companies
for short_symbol, ticker in companies.items():
    # Link to the news page
    link = f"https://www.moneycontrol.com/news/{ticker}/business-{short_symbol}-6months.html"

    # Send the request and get the response
    r = session.get(link)

    # Check if the response is successful
    if r.status_code == 200:
        # Scrape the news
        for i in range(100):
            try:
                news_element = r.html.find(f"#newslist-{i}", first=True)  # Find the news element

                if news_element:
                    news_text = str(news_element.text).replace("\n", ".")

                    # Extract timestamp using regular expression
                    time_element = news_element.find(".clip-dt", first=True)  #Find the timestamp element
                    if time_element:
                        timestamp_text = time_element.text
                    else:
                         timestamp_text = None  # If no time element is found, set to None

                    all_news_data.append({
                        'news': news_text,
                        'short_symbol': short_symbol,
                        'ticker': ticker,
                        'timestamp': timestamp_text  # Add timestamp to data
                    })
                else:
                    break  # Break the loop if no more news articles are found
            except Exception as e:
                print(f"Error fetching news article {i} for {ticker}: {e}")

        print(f"News for {ticker} fetched successfully.")
    else:
        print(f"Failed to retrieve data for {ticker}. Status code: {r.status_code}")

# Create a DataFrame from the collected data
news_df = pd.DataFrame(all_news_data)

# Fetch timestamp in yyyymmddhhmmss format and add to the file name
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")
file_name = f"news_sentiment_{timestamp}.csv"

# Save to CSV to the project path
news_df.to_csv(f"{path}{file_name}", index=False)

print("News sentiment data saved to CSV.")