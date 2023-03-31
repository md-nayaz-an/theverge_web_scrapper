<<<<<<< HEAD
from distutils.file_util import write_file
import requests, bs4
from selenium import webdriver
from regex import Regex
=======
import requests, bs4, csv, sqlite3
from selenium import webdriver
from regex import Regex
from datetime import datetime

>>>>>>> main

re = Regex()

class scraper():
  url = ""
  res = ''
<<<<<<< HEAD

  def __init__(self, url):
    self.url = url
    self.browser = webdriver.Firefox()
    self.browser.get(self.url)
    self.writeFile()
=======
  cursor = None

  def __init__(self, url):
    self.url = url

    #self.browser = webdriver.Firefox()
    #self.browser.get(self.url)
    #self.writeFile()

    self.conn = sqlite3.connect('database/verge_scrap.db')
    self.cursor = self.conn.cursor()

    self.cursor.execute('''CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            URL TEXT UNIQUE,
                            headline TEXT,
                            author TEXT,
                            date DATE)''')

>>>>>>> main
    self.readFile()
    self.getSoup()

  def writeFile(self):
<<<<<<< HEAD
    f = open("responsefile.html", "w")
    f.write(self.browser.page_source)
  
  def readFile(self):
    self.res = open("responsefile.html", "r").read()
    
  def soupRelativeAuthor(self, articleStarch):
    
    found = False

    for parent in articleStarch.parents:
      hrefrelsoup = parent.find_all('a')

      for i in hrefrelsoup:
        if(re.authorRegex(i.get('href'))):
          print(i.get('href'))
          found = True
          input()
        if(found):
          break
      
      if(found):
        break
    
    if not found:
      print("author not found")
          

  def getSoup(self):
    soup = bs4.BeautifulSoup(self.res, 'html.parser')

    tag = input("Enter the tag format to find:")

    starch = soup.find_all(tag)

    links = []

    for i in range(len(starch)):
      hrefurl = starch[i].get('href')
      nexthrefurl = starch[i+1].get('href')
      
      if(hrefurl == nexthrefurl):
        continue
      #print(hrefurl)
      
      if(re.nondatedUrlRegex(hrefurl)):
        
        '''if(re.datedUrlRegex(hrefurl)):
          print('########## dated ARTICLE #######')
        else:
          print('########## ARTICLE #############')
        '''

        links.append(hrefurl)
        print(starch[i].getText())
        print(hrefurl)

        self.soupRelativeAuthor(starch[i])

        #print(starch[i].getText())
        
        
        input()
      
      '''if(re.authorRegex(hrefurl)):
        print(hrefurl)
        for parent in starch[i].parents:
          print(parent.name, end='->')
        print()
        input()'''

=======
    date = datetime.now().strftime("%d%m%y")
    f = open(f"html_src_content/responsefile{date}.html", "w")
    f.write(self.browser.page_source)
  
  def readFile(self):
    date = datetime.now().strftime("%d%m%y")
    self.res = open(f"html_src_content/responsefile{date}.html", "r").read()

  def printContent(self, key, starch):
    print(key + ': ' + starch.get('content'))

  def getSoup(self):
    tag = 'a'

    soup = bs4.BeautifulSoup(self.res, 'html.parser')
    starch = soup.find_all(tag)

    links = []
    id = 0

    date = datetime.now().strftime("%d%m%y")
    #file = open(f'csv/{date}_verge.csv', 'w')
    headers = ['id', 'URL', 'headline', 'author', 'date']
    #writer = csv.DictWriter(file, fieldnames=headers)
    #writer.writeheader()


    for i in range(len(starch)):
      hrefurl = starch[i].get('href')
      
      if(hrefurl in links):
        continue

      if(re.nondatedUrlRegex(hrefurl)):
        id += 1    
        links.append(hrefurl)
        print(hrefurl)

        pageres = requests.get("http://theverge.com" + hrefurl)
        pagesoup = bs4.BeautifulSoup(pageres.content, 'html.parser')
        
        authorStarch = pagesoup.find_all('meta', {'name' : 'parsely-author'})
        titleStarch = pagesoup.find('meta', {'name' : 'parsely-title'})
        linkStarch = pagesoup.find('meta', {'name' : 'parsely-link'})
        dateStarch = pagesoup.find('meta', {'name' : 'parsely-pub-date'})

        url = linkStarch.get('content')
        headline = titleStarch.get('content')
        author = []        
        date = dateStarch.get('content')[:10]

        for a in authorStarch:
          author.append(a.get('content'))
        author = ", ".join(author)

        print('id: ' + str(id))
        print('url: ' + url)
        print('headline: ' + headline)
        print('author: ' + author)
        print('date: ' + date[:10])
        print()

        '''
        writer.writerow({
          'id': id,
          'URL': url,
          'headline': headline,
          'author': author,
          'date': date
        })

        self.cursor.execute('''INSERT OR IGNORE INTO articles
                  (URL, headline, author, date)
                  VALUES(?, ?, ?, ?)''',
                  (url, headline, author, date))
'''
    self.conn.commit()
    self.conn.close()

        
>>>>>>> main
   
if __name__ == "__main__":
  url = "http://theverge.com"
  scraper(url)