from dump_article.dump_html import DumpITWorld

articles = DumpITWorld("http://www.itworld.com/news")
#get_articles = articles.get_clean_articles(10)

for title in articles.get_popular_articles_titles(reverse=True):
    print title

"""fo = open("foo.txt", "w+")

for title, content in get_articles:
    fo.write("\ntitle\n")
    fo.write(str(title))
    fo.write("\n")
    fo.write(str(content))
    
fo.close()
"""