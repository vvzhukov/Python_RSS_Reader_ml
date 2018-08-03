import feedparser

rss = 'http://www.blog.pythonlibrary.org/feed/'
feed = feedparser.parse(rss)
for key in feed["entries"]:
    print((key["title"]))

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(feed)
