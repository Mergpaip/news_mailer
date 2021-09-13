import requests
from bs4 import BeautifulSoup
import pandas as pd

def send_request(url):

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    return(soup)

####################################################################################################################

def parse_NOS():

    results = []

    soup = send_request("https://nos.nl/nieuws/buitenland")
 
    articles = soup.find_all('a', attrs={'class': 'link-block list-items__link'})

    for article in articles:

        if len(results) < 10:

            article_link = 'https://nos.nl'+article['href']
            article_title = article.find('h3', attrs={'class': 'list-items__title list-items__link-hover'}).text.strip()
            article_combined = '<a href='+article_link+'>'+article_title+'</a><br><br>'
            
            results.append([article_combined])

    df = pd.DataFrame(columns= ['article_combined'], data=results)
    
    return df.to_string(index=False, header=False)

#############################################################################################################

def parse_NRC():

    results = []

    soup = send_request("https://www.nrc.nl/index/buitenland/meer/")

    articles = soup.find_all('a', attrs={'class': 'nmt-item__link'})

    for article in articles:

        if len(results) < 10:

            article_link = 'https://www.nrc.nl'+article['href']
            article_title = article.find('h3', attrs={'class': 'nmt-item__headline'}).text.strip()
            article_combined = '<a href='+article_link+'>'+article_title+'</a><br><br>'

            results.append([article_combined])

    df = pd.DataFrame(columns= ['article_combined'], data=results)
    
    return df.to_string(index=False, header=False)

####################################################################################################

def parse_AJ():

    results = []

    soup = send_request("https://www.aljazeera.com/news/")

    articles = soup.find_all('h3', attrs={'class': 'gc__title'})

    for article in articles:

        if len(results) < 10:

            article_link = 'https://www.aljazeera.com'+article.find('a')['href']
            article_title = article.find('a').text.strip()
            article_combined = '<a href='+article_link+'>'+article_title+'</a><br><br>'

            results.append([article_combined])

    df = pd.DataFrame(columns= ['article_combined'], data=results)
    
    return df.to_string(index=False, header=False)

####################################################################################################

def parse_FT():

    results = []

    soup = send_request("https://www.ft.com/world/")

    articles = soup.find_all('a', attrs={'class': 'js-teaser-heading-link'})

    for article in articles:

        if len(results) < 10:
            
            article_link = 'https://www.ft.com'+article['href']
            article_title = article.text.strip()
            article_combined = '<a href='+article_link+'>'+article_title+'</a><br><br>'

            results.append([article_combined])

    df = pd.DataFrame(columns= ['article_combined'], data=results)
    
    return df.to_string(index=False, header=False)

####################################################################################################

def parse_Trouw():

    results = []

    soup = send_request("https://www.trouw.nl/sections/buitenland")

    articles = soup.find_all('article')

    for article in articles:

        if len(results) < 10:

            article_title = article.find('span', attrs={'class': 'teaser__title__value--long'}).text.strip()
            article_link = 'https://www.trouw.nl'+article.find('a')['href']

            article_combined = '<a href='+article_link+'>'+article_title+'</a><br><br>'       

            results.append([article_combined])

    df = pd.DataFrame(columns= ['article_combined'], data=results)
    
    return df.to_string(index=False, header=False)

####################################################################################################

from datetime import date

today = date.today()
DATE = str(today.strftime("%d %B %Y"))

###################################################################################################

import smtplib
from email.message import EmailMessage

def send_email():

    #make new gmail (don't use your own) and allow 'less secure apps' in settings
    GMAIL_USERNAME = 'YOUR_GMAIL' #adjust
    GMAIL_PASSWORD = 'YOUR_PASSWORD' #adjust


    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)


    msg = EmailMessage()
    msg['Subject'] =  'Global news update ' + DATE
    msg['From'] = GMAIL_USERNAME 
    msg['To'] = 'EMAIL_RECIPIENT' #adjust
    msg.set_content('The HTML is not loaded correctly.')


    msg.add_alternative(f'''\n\n

<body>
    <div class="container">
        <h2 style = color:#363636 class="ax-center text-white text-center mb-10">Daily global news update</h2>
        <h3 style = color:#363636 class="ax-center text-white text-center mb-10">''' + DATE + '''</h3>
        
        <h4 style = color:#cd171e style="margin:35px 0;" class="ax-center max-w-128 text-white text-center">NOS</h4>
        
''' + parse_NOS() + '''

        <h4 style = color:#cd171e style="margin:35px 0;" class="ax-center max-w-128 text-white text-center">Financial Times</h4>

''' + parse_FT() + '''
        
        <h4 style = color:#cd171e style="margin:35px 0;" class="ax-center max-w-128 text-white text-center">NRC</h4>

''' + parse_NRC() + '''

        <h4 style = color:#cd171e style="margin:35px 0;" class="ax-center max-w-128 text-white text-center">Trouw</h4>

''' + parse_Trouw() + '''
        
        <h4 style = color:#cd171e style="margin:35px 0;" class="ax-center max-w-128 text-white text-center">Al Jazeera</h4>

''' + parse_AJ() + '''

    </div>
  </body>
  
''', subtype='html')


    smtp.send_message(msg)


###################################################################################################

import time

while True:

    t = time.localtime()

    current_time = time.strftime("%H:%M:%S", t)

    if str(current_time) == "07:00:00":

        send_email()

        time.sleep(10)

    time.sleep(0.5)