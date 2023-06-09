import requests, bs4, csv, sqlite3, pytz
from selenium import webdriver
from regex import Regex
from datetime import datetime
from selenium.webdriver.firefox.options import Options

re = Regex()
ist = pytz.timezone('Asia/Kolkata')

class scraper():
  url = ""
  res = ''
  cursor = None

  def __init__(self, url):
    self.url = url

    options = Options()
    options.headless = True
    self.browser = webdriver.Firefox(options=options)
    self.browser.get(self.url)
    self.writeFile()

    self.conn = sqlite3.connect('database/verge_scrap.db')
    self.cursor = self.conn.cursor()

    self.cursor.execute('''CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            URL TEXT UNIQUE,
                            headline TEXT,
                            author TEXT,
                            date DATE)''')

    self.readFile()
    self.getSoup()

  def writeFile(self):
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
    file = open(f'csv/{date}_verge.csv', 'w')
    headers = ['id', 'URL', 'headline', 'author', 'date']
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()


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

    self.conn.commit()
    self.conn.close()
    
    print("\n***********************************************************")
    print(datetime.now(ist).isoformat() + "\t 'Updated CSV and Database'")
    print("***********************************************************\n")
        
   
if __name__ == "__main__":
  url = "http://theverge.com"
  scraper(url)