'''
Created on Apr 20, 2015

@author: ruby
'''

# news_articles.categories = ['politics','health', 'business', 'technology', 'sports','entertainment]

from newspaper import Article
import newspaper

paper = newspaper.build('http://www.state.gov/p/')
print(paper.articles.__len__())

headline_file = open("../resources/headlines/h_1.txt", "a")
news_file = open("../resources/news/n_1.txt", "a")
cnt = 1
for a in paper.articles:
    url = a.url
    article = Article(url, language='en')
    article.download()
    article.parse()
    headline = article.title
    news = article.text
    if(news.__len__() > 256 and headline.__len__() > 1 and not 'Page not found' in headline):
        print("Writing %d " %cnt)
        cnt += 1
        headline_file.write(headline.encode('ascii','ignore'))
        headline_file.write("\n")
        news_file.write(news.encode('ascii', 'ignore'))
        news_file.write("\n BREAKS HERE")
headline_file.close()
news_file.close()