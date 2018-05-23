#a tiny class that takes a latex file, identifies the citations, and returns the relevant bibtex entries using ADS. It assumes each citation key to be something like <name of first author><year>. It will return all bibtex entries found for the query, so the user has to delete the unnecessary ones afterwards.

from ads_api_key import api_key
import ads
import re 
ads.config.token = api_key
class referenceWizard(object):
    def __init__(self,fname_tex,fname_exclude=None,verbose=True):
        self.verbose = verbose
        self.load_refs(fname_tex)
        self.decypher_refs()
        if(fname_exclude is not None):
            self.exclude_some(fname_exclude)
        self.load_bibtex()
    def exclude_some(self,fname_exclude):
        import bibtexparser
        if(not isinstance(fname_exclude,list)):
            fname_exclude = [fname_exclude]
        for fname in fname_exclude:
            with open(fname) as bibtex_file:
                bibtex_database = bibtexparser.load(bibtex_file,parser=bibtexparser.bparser.BibTexParser(common_strings=True))
            for key in bibtex_database.entries_dict.keys():
                if(key in self.decyphered_refs):
                    if(self.verbose):
                        print "Ignoring key",key
                    del self.decyphered_refs[key]
    def load_refs(self,fname_tex):
        self.refs={}
        rcite = re.compile(r"\\(cite|citep|citet)[(\[\])]*\{([^\}]+).*?")
        with open(fname_tex,"r") as f:
            lines = f.readlines()
        for line in lines:
            m=rcite.findall(line)
            for match in m:
                if("," in match[1]):
                    for single_match in match[1].split(","):
                        self.refs[single_match] = None
                else:
                    self.refs[match[1]] = None
    def decypher_refs(self):
        self.decyphered_refs = {}
        rcypher = re.compile(r"(\D+?)(\d+)")
        for ref in self.refs.keys():
            m = rcypher.match(ref)
            if(m is not None):
                self.decyphered_refs[ref] = m.groups()
            else:
                self.decyphered_refs[ref] = m
        #print self.decyphered_refs
    def load_bibtex(self):
        self.bibcodes=[]
        temp_keys =[]
        for key, value in self.decyphered_refs.iteritems():
            if(value is None):
                print "Could not determine an entry for",key
            else:
                papers = list(list(ads.SearchQuery(first_author=value[0],year=int(value[1]),database="astronomy")))
                #print "for",value
                #for paper in papers:
                #    print "\t",paper.author, paper.bibcode
                for paper in papers:
                    self.bibcodes.append(paper.bibcode)
                    temp_keys.append([key,paper.bibcode])
        exp=ads.export.ExportQuery(self.bibcodes)
        self.bibs = exp.execute()
        for i,key in enumerate(temp_keys):
            self.bibs = self.bibs.replace("{"+key[1],"{"+key[0])
            
            
