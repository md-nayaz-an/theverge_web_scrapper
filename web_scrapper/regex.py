import re

class Regex():
  def datedUrlRegex(self, urlText):
    urlRegex = re.compile(r'^/\d{4}/\d{1,2}/\d{2}/')
    result = urlRegex.match(urlText)

    if result:
      return True
    else:
      return False

  def authorRegex(self, urlText):
    urlRegex = re.compile(r'^/authors/')
    result = urlRegex.match(urlText)

    if result:
      return True
    else:
      return False


  def nondatedUrlRegex(self, urlText):
    urlRegex = re.compile(r'^/\d+/')
    result = urlRegex.match(urlText)

    if result:
      return True
    else:
      return False
