from ads_api_key import api_key
fields = ['id', 'bibcode', 'title', 'citation_count','pub','author','year','first_author','volume','page','title']
def load_refs(author,is_first_author=False):
    '''load the bibliography of author from ads. return list of references.'''
    import ads
    ads.config.token = api_key
    #import ads.sandbox as ads
    if(is_first_author):
        return list(list(ads.SearchQuery(first_author=author,database="astronomy",fl=fields)))    
    else:
        return list(list(ads.SearchQuery(author=author,database="astronomy",fl=fields)))
    


def format_line_long(article):
    '''format a line for article, in long form'''
    #format authors
    s=""
    for author in article.author:
        s+=author+", "
    #add title
    s += "\""+article.title[0]+"\","
    #add journal etc
    if(article.pub is not None):
        s+=" in: "+article.pub
    if(article.volume is not None):
        s+=", "+article.volume
    if(article.page is not None):
        s+=", "+article.page[0]
    if(article.year is not None):
        s+=", ("+article.year+")"
    return s
def format_line_short(article):
    '''format a line for article, in short form'''
    s=""
    nauthors = len(article.author)
    if(nauthors==2):
        s += article.author[0]+" & "+article.author[1]
    elif(nauthors>3):
        s+= article.author[0]+" et al."
    else:
        for author in article.author:
            s+=author+" "
    s+=" ("+article.year+"), "    
    #add journal etc
    if(article.pub is not None):
        s+=article.pub
    if(article.volume is not None):
        s+=", "+article.volume
    if(article.page is not None):
        s+=", "+article.page[0]
    return s
        
def preprocess(article):
    '''replace journal names by their acronym'''
    if("Monthly Notices of the Royal Astronomical Society" in article.pub):
        article.pub = "MNRAS"
    if("Astronomy and Astrophysics" in article.pub):
        article.pub = "A&A"
    return article


def by_citation(a):
    return a.citation_count
def by_year(a):
    return a.year

def get_bibliography(author, is_first_author=False, only_second_authors=False, sort_by=by_year,the_format="long"):
    '''get the bibliography for author. Only include first author papers if is_first_author. 
    Only include papers where is author is second/third/... author if only_second_authors. '''
    query=load_refs(author,is_first_author=is_first_author)
    sorted_query = sorted(query,reverse=False,key=sort_by)
    s = ""
    for article in sorted_query:
        if(only_second_authors):
            if(article.author[0]==author):
                continue
        if("long" in the_format):
            mys = format_line_long(preprocess(article))
        elif("short" in the_format):
            mys = format_line_long(preprocess(article))
        else:
            raise NameError("Unknown format")
        #print mys
        s += mys+"\n"
    return s

if(__name__=="__main__"):
    import sys
    bib=get_bibliography(sys.argv[1],only_second_authors=sys.argv[2])
    print bib


    

