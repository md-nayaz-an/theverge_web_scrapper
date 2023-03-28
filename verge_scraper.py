from distutils.file_util import write_file
import requests, bs4
from selenium import webdriver
from regex import Regex

re = Regex()

class scraper():
  url = ""
  res = ''

  def __init__(self, url):
    self.url = url
    self.browser = webdriver.Firefox()
    self.browser.get(self.url)
    self.writeFile()
    self.readFile()
    self.getSoup()

  def writeFile(self):
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

   
if __name__ == "__main__":
  url = "http://theverge.com"
  scraper(url)