%pip install requests bs4 lxml requests_html pandas

import pandas as pd
import requests
import bs4
import lxml
import time
from requests_html import HTMLSession

session=HTMLSession()
news=list()
news_sentiment=pd.DataFrame()
ticker="tataconsultancyservices"
short_symbol="TCS"
news=list()
link=f"https://www.moneycontrol.com/news/{ticker}/business-{short_symbol}-6months.html"
r=session.get(link)
k=len(r.html.links)
for i in range(100):
            about=r.html.find(f"#newslist-{i}",first=True)
            l=about.text
            x=str(l)
            x=x.replace("\n",".")
            news.append(x)
            # time.sleep(10)
print(news)
news_sentiment[ticker]=news
news_sentiment.to_csv("news_sentiment.csv")
news_sentiment

