from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import requests
from bs4 import BeautifulSoup

# Create your views here.
def show(request):
    today = date.today()
    res = requests.get('https://news.ycombinator.com/news')
    bs = BeautifulSoup(res.text, 'html.parser')
    links = bs.select('.storylink')
    subtext = bs.select('.subtext')
    news = collect_news(links,subtext)
    return render(request,'index.html',{'today':today,'news':news[:20]})

def collect_news(links,subtext):
    news = []
    for i,item in enumerate(links):
        title = item.getText()
        href = item.get('href',None)
        vote = subtext[i].select('.score')
        if len(vote):
            score = int(vote[0].getText().replace(' points',''))
            if score >= 25:
                news.append({'title':title,'score':score,'href':href})
    return sorted(news,key=lambda k:k['score'],reverse=True)