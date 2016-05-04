def loadStopWords(stopWordFile):
    stopWords = []
    for line in open(stopWordFile):
        if (line.strip()[0:1] != "#"):
            for word in line.split( ): #in case more than one per line
                stopWords.append(word)
    return stopWords


def buildStopwordRegExPattern(pathtostopwordsfile):
      stopwordlist = loadStopWords(pathtostopwordsfile)
      stopwordregexlist = []
      for wrd in stopwordlist:
          wrdregex = '\\b' + wrd + '\\b'
          stopwordregexlist.append(wrdregex)
      stopwordpattern = re.compile('|'.join(stopwordregexlist), re.IGNORECASE)
      return stopwordpattern

