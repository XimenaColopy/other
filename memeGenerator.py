
import requests
from bs4 import BeautifulSoup
import random
import yagmail
from datetime import date
import mysql.connector
import os
import time

headers = {
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
}


def main():
    i = random.randint(0, 2)
    if i == 0:
        image = pandaMemes()
    elif i == 1:
        image = awesomeDailyMemes()
    elif i == 2:
        image = rockleMemes()
    downloadImage(image)
    print(image)
    sendEmail()

def downloadImage(image):
    r = requests.get(image, headers=headers, timeout=5)
    time.sleep(5)
    if r:
        with open('pic.jpg', "wb") as f:
            f.write(r.content)
    else:
        print('error')
       

def scrapeLink(url):
    res = requests.get(str(url), headers=headers, timeout=5)
    soup = BeautifulSoup(str(res.text), features="html.parser")
    return soup

def pandaMemes():
    url =  'https://www.boredpanda.com/unspirational-quotes-instagram/'
    soup = scrapeLink(url)
    results = soup.find_all('span', attrs={"class":"shareable-image-block"})
    i = random.randint(0, len(results)-1)
    tag = results[i].find('img')
    return tag['src']

def awesomeDailyMemes():
    url = 'https://theawesomedaily.com/20-uninspirational-quotes-that-tell-it-like-it-is/'
    soup = scrapeLink(url)
    results = soup.find_all("img", attrs={"alt":"uninspirational quotes"})
    i = random.randint(0, len(results)-1)
    return results[i]['src']

def rockleMemes():
    url = 'https://therockle.com/demotivational-quotes/'
    soup = scrapeLink(url)
    results = soup.find_all('div', attrs={"class":"wp-block-image"})
    i = random.randint(0, len(results)-1)
    tag = results[i].find('img')
    return tag['src']

def sendEmail():

    mydb = mysql.connector.connect(host="localhost", user="ximena", password="Horse4horse")
    mycursor = mydb.cursor()
    db_statement = "use other"
    mycursor.execute(db_statement)
    sql = "select email from meme_emails"
    mycursor.execute(sql)
    emails = mycursor.fetchall() 

    subject='Daily Demotivation for {}'.format(date.today())
    content = [
	"Here is your uninspirational quote of the day"
        "\n-Enjoy!" 
    ]

    for person in emails:
        try:
            person = person[0] #the way it is extracted from the database is a list of tuples
            #initializing the server connection
            yag = yagmail.SMTP(user='ximenabotbot@gmail.com', password='Twitterbot')
            #sending the email
            yag.send(to=person , subject=subject, contents=content, attachments = '/home/ximena/pic.jpg')
            print("Email sent successfully")
        except:
            print("Error, email was not sent")


main()
