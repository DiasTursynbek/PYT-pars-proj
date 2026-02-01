import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
from bs4 import BeautifulSoup
import schedule
import time
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '8562911161:AAHIoLgdkdn8UTLbhQdKAaY3Y6nbiFDhMEk'

urls = [
    "https://digitalbusiness.kz",
    "https://er10.kz",
    "https://the-tech.kz",
    "https://www.spot.uz",
    "https://limon.kg",
    "https://bluescreen.kz",
    "https://astanahub.com",
    "https://it-park.uz",
    "https://it-park.kg",
    "https://most.com.kz",
    "https://forbes.kz",
    "https://kursiv.media",
    "https://weproject.media",
    "https://asiaplustj.info",
    "https://profit.kz"
]

keywords = ['инвестиции', 'раунд', 'экзит', 'технологические прорывы']

sent_articles = set()

def parse_digitalbusiness():
    url = "https://digitalbusiness.kz"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = soup.find_all('h3', class_='entry-title')
    articles = []

    for headline in headlines:
        title = headline.get_text(strip=True)
        link = headline.find('a')['href']
        description = headline.find_next('p').get_text(strip=True)
        date = headline.find_next('time')['datetime']
        articles.append({
            "title": title,
            "link": link,
            "description": description,
            "date": date
        })
    
    return articles

def parse_er10():
    url = "https://er10.kz"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = soup.find_all('h2', class_='post-title')
    articles = []

    for headline in headlines:
        title = headline.get_text(strip=True)
        link = headline.find('a')['href']
        description = headline.find_next('p').get_text(strip=True)
        date = headline.find_next('time')['datetime']
        articles.append({
            "title": title,
            "link": link,
            "description": description,
            "date": date
        })
    
    return articles

def parse_the_tech():
    url = "https://the-tech.kz"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = soup.find_all('h2', class_='entry-title')
    articles = []

    for headline in headlines:
        title = headline.get_text(strip=True)
        link = headline.find('a')['href']
        description = headline.find_next('p').get_text(strip=True)
        date = headline.find_next('time')['datetime']
        articles.append({
            "title": title,
            "link": link,
            "description": description,
            "date": date
        })
    
    return articles

def parse_spot_uz():
    url = "https://www.spot.uz"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = soup.find_all('h2', class_='post-title')
    articles = []

    for headline in headlines:
        title = headline.get_text(strip=True)
        link = headline.find('a')['href']
        description = headline.find_next('p').get_text(strip=True)
        date = headline.find_next('time')['datetime']
        articles.append({
            "title": title,
            "link": link,
            "description": description,
            "date": date
        })
    
    return articles

def parse_limon():
    url = "https://limon.kg"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = soup.find_all('h3', class_='entry-title')
    articles = []

    for headline in headlines:
        title = headline.get_text(strip=True)
        link = headline.find('a')['href']
        description = headline.find_next('p').get_text(strip=True)
        date = headline.find_next('time')['datetime']
        articles.append({
            "title": title,
            "link": link,
            "description": description,
            "date": date
        })
    
    return articles

def parse_site(url):
    if "digitalbusiness.kz" in url:
        return parse_digitalbusiness()
    elif "er10.kz" in url:
        return parse_er10()
    elif "the-tech.kz" in url:
        return parse_the_tech()
    elif "spot.uz" in url:
        return parse_spot_uz()
    elif "limon.kg" in url:
        return parse_limon()
    else:
        return []

def filter_news(news):
    filtered_news = []
    for article in news:
        if any(keyword in article['title'].lower() or keyword in article['description'].lower() for keyword in keywords):
            filtered_news.append(article)
    return filtered_news

def remove_duplicates(news):
    global sent_articles
    unique_news = []
    for article in news:
        article_id = article['title'] + article['link']
        if article_id not in sent_articles:
            unique_news.append(article)
            sent_articles.add(article_id)
    return unique_news

async def send_news(update: Update, context: CallbackContext):
    news = []
    for url in urls:
        news.extend(parse_site(url))
    
    filtered_news = filter_news(news)
    unique_news = remove_duplicates(filtered_news)
    
    sorted_news = sorted(unique_news, key=lambda x: x['date'], reverse=True)[:5]
    formatted_news = "\n\n".join([f"{article['title']}\n{article['link']}\n{article['description']}\nДата: {article['date']}" for article in sorted_news])
    
    await update.message.reply_text(formatted_news)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Я твой бот для новостей. Введи /news, чтобы получить свежие новости.')

def send_daily_digest():
    news = []
    for url in urls:
        news.extend(parse_site(url))
    
    filtered_news = filter_news(news)
    unique_news = remove_duplicates(filtered_news)
    
    sorted_news = sorted(unique_news, key=lambda x: x['date'], reverse=True)[:5]
    formatted_news = "\n\n".join([f"{article['title']}\n{article['link']}\n{article['description']}\nДата: {article['date']}" for article in sorted_news])

    subscribers = []
    for user in subscribers:
        user.send_message(formatted_news)

schedule.every().day.at("09:00").do(send_daily_digest)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('news', send_news))

    application.run_polling()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()