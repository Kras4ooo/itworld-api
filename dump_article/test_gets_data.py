from dump_article.dump_html import DumpITWorld

articles = DumpITWorld("http://www.itworld.com/news")
#get_articles = articles.get_clean_articles(10)

fo = open("foo.txt", "w+")

for title, content in articles.get_popular_articles(reverse=True):
    fo.write("\ntitle\n")
    fo.write(str(title))
    fo.write("\n")
    fo.write(str(content))
    
fo.close()
