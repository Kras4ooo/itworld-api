from dump_article.dump_html import DumpITWorld

articles = DumpITWorld("http://www.itworld.com/news")
get_articles = articles.get_clean_articles()

fo = open("foo.txt", "w+")

for title, content in get_articles:
    fo.write("\ntitle\n")
    fo.write(str(title))
    fo.write("\n")
    fo.write(str(content))
    
fo.close()