#http://dlab.berkeley.edu/blog/scraping-new-york-times-articles-python-tutorial

from datetime import datetime
from nytimesarticle import articleAPI
from nltk.tag import pos_tag
from nltk.tree import Tree
from nltk.chunk import ne_chunk
import time


def parse_articles(articles):
    news = []
    for i in articles['response']['docs']:
        dic = {}
        dic['url'] = i['web_url']
        dic['headline'] = i['headline']['main'].encode("utf8")
        dic['section'] = i['section_name']
        dic['lead'] = i['lead_paragraph']
        #dic['author'] = i['byline']['original'].encode("utf8")
        if dic['section'] != None:
            news.append(dic)
    return(news)
       
def get_articles(api, section):
    curr_date = datetime.now()
    format_date = curr_date.strftime("%Y%m%d")

    all_articles = []
    for i in range(0, 2):
        articles = api.search(fq = {'section_name':section},
            begin_date = format_date,
            sort = 'oldest',
            page = str(i))
        if articles:
            articles = parse_articles(articles)
        else:
            break
        all_articles = all_articles + articles
        time.sleep(1)

    return(all_articles)

def which_sections():
    print "New York Times Sections: "
    sections_list = ["NY / Region", "Sports", "U.S.", "Business Day", "Arts", "Health", "World", "Technology", "Opinion", "Theater", "Books", "Today's Paper", "Crosswords & Games", "Fashion & Style", "Travel", "Briefing", "The Learning Network", "The Upshot", "Real Estate", "Well", "Podcasts", "Multimedia/Photos", "T Magazine", "Times Insider", "Science", "Climate"]

    count = 1
    for i in sections_list:
        print str(count) + ": " + i
        count += 1
    
    print

    section = []
    while True:
        section_input = raw_input("Please pick a section, type Done if out of sections: ")
        if section_input == "Done": break
        sanitize_section_input(section_input, section)
    return(section)


def sanitize_section_input(sinput, section):
    if sinput == 'NY / Region' or sinput == '1' :
        section.append('N.Y.')
    elif sinput == 'Sports' or sinput == '2':
        section.append('Sports')
    elif sinput == 'U.S.' or sinput == '3':
        section.append('U.S.')
    elif sinput == 'Business Day' or sinput == '4':
        section.append('Business')
    elif sinput == 'Arts' or sinput == '5':
        section.append('Arts')
    elif sinput == 'Health' or sinput == '6':
        section.append('Health')
    elif sinput == 'World' or sinput == '7':
        section.append('World')
    elif sinput == 'Technology' or sinput == '8':
        section.append('Technology')
    elif sinput == 'Opinion' or sinput == '9':
        section.append('Opinion')
    elif sinput == 'Theater' or sinput == '10':
        section.append('Theater')
    elif sinput == 'Books' or sinput == '11':
        section.append('Books')
    elif sinput == "Today's Paper" or sinput == '12':
        section.append('Paper')
    elif sinput == 'Crosswords & Games' or sinput == '13':
        section.append('Crosswords')
    elif sinput == 'Fashion & Style' or sinput == '14':
        section.append('Fashion')
    elif sinput == 'Travel' or sinput == '15':
        section.append('Travel')
    elif sinput == 'Briefing' or sinput == '16':
        section.append('Briefing')
    elif sinput == 'The Learning Network' or sinput == '17':
        section.append('Learning')
    elif sinput == 'The Upshot' or sinput == '18':
        section.append('Upshot')
    elif sinput == 'Real Estate' or sinput == '19':
        section.append('Estate')
    elif sinput == 'Well' or sinput == '20':
        section.append('Well')
    elif sinput == 'Podcasts' or sinput == '21':
        section.append('Podcasts')
    elif sinput == 'Multimedia/Photos' or sinput == '22':
        section.append('Multimedia')
    elif sinput == 'T Magainze' or sinput == '23':
        section.append('Magazine')
    elif sinput == 'Times Insider' or sinput == '24':
        section.append('Insider')
    elif sinput == 'Science' or sinput == '25':
        section.append('Science')
    elif sinput == 'Climate' or sinput == '26':
        section.append('Climate')

def get_proper_nouns(alist): 
    proper_list = []
    count = 0
    for i in alist:
        phrase = i['lead']
        head_tags = pos_tag(phrase.split())
        p_n = [word for word, pos in head_tags if pos == 'NNP']
        proper_list.append(p_n)
        
        print str(count + 1) + ": " + i['headline']
        print "     url: " + i['url']
        print

        count += 1
    return proper_list

def main():
    txt = open("keywords.txt", "w")

    api = articleAPI('45862958eff543bb9555201274493184')
    sections = which_sections()
    article_list = get_articles(api, sections)

    proper_list = get_proper_nouns(article_list)
    
    pref_list = []
    while True:
        pref = raw_input("Which articles sound interesting? ")
        if pref == '-': break
        pref_num = int(pref) - 1
        for i in proper_list[pref_num]:
            txt.write(i + '\n')


if __name__ == '__main__':
    main()
