# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 17:03:42 2021

@author: peter
"""

#Requests is used to pull HTML from the URL, BeautifulSoup is used to parse the HTML, and time is specifically for this use case to test for After Hours trading.
import requests
from bs4 import BeautifulSoup
import time

#Header required to pretend you're a webbrowser and not a bot.
headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://www.google.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }


def price(ticker, exchange):
    #This list is where I'm placing all the text I'm extracting from the html.
    memo = []

    #These three lines are standard for any scraper.
    url = "https://www.google.com/finance/quote/{}:{}".format(ticker, exchange)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    #Appending to memo the previous close price. Note there is consistent use of text.replace() to remove unwanted chars
    previous_close = [tag for tag in soup.find_all(attrs={'class': 'P6K39c'}) if '$' in tag.text]
    memo.append(float(previous_close[0].text.replace('<div class="P6K39c">','').replace('</div>',"").replace('$','')))
    
    #Appending to memo the current market price. Note there is consistent use of text.replace() to remove unwanted chars
    market_price = soup.find_all("div", attrs={"class": "YMlKec fxKbKc"})
    memo.append(float(market_price[0].text.replace("$","")))
    
    #As I want to identify after hours prices, I have imported time so I can tell if we're AH or not.
    local_time = int(time.strftime("%H%M", time.localtime()))
    
    #If After Hours, then it picks up a different price under a different reference. Otherwise, carry on as normal.
    if 830 <= local_time <= 1500:
        pass
    else:
        after_hours = soup.find_all("span", attrs={"class": "tO2BSb eExqnb DnMTof"})
        memo[-1] = float(after_hours[0].text.replace("$",""))
    
    #Extracting the information I've put into memo, and doing the math inside the print statement for % increase.
    if local_time < 830 or local_time >= 1500:
        print(ticker + ": $" + str(memo[-1]) + " AH " + str(round(((memo[-1]-memo[0])/memo[0])*100,2)) + "% change (Previous close: " + str(memo[0]) + ")")
    else:
        print(ticker + ": $" + str(memo[-1]) + " " + str(round(((memo[-1]-memo[0])/memo[0])*100,2)) + "% change (Previous close: " + str(memo[0]) + ")")
        

# When a Python interpreter reads a source file it executes all its code.
# This __name__ check makes sure this code block is only executed when this
# module is the main program. 
if __name__ == '__main__':
    price("GME", "NYSE")
    price("TSLA", "NASDAQ")
    price("INTC", "NASDAQ")