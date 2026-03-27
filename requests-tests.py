import requests

URL = "https://en.wikipedia.org/w/api.php"




class wikitool:
    def __init__(self):
        
         
        self.header = {
        "User-Agent": 'SchoolProject-COMPSCI/1.0 (High School Project; Fairveiw High School; mailto: rpvarma01@bvsd.org)'
        }
        self.articles = []
        self.choice_index = 0
        self.title = ""
        self.article_chosen = False
        self.fullText = ""
         
    def wiki_search(self, search):
        params_search = {
            "action": "query",
            "list": "search",
            "srsearch": search,
            "srlimit": 10,
            "format": "json"}
        
        response = requests.get(URL, headers= self.header, params = params_search)
        response.raise_for_status()

        data  = response.json()

        titles = [item["title"] for item in data["query"]["search"]]
        self.articles = titles
        return self.articles


    def wiki_choose(self, choice):
        if (self.articles == []):
            return "error no loaded article"
        else:
            self.choice_index = choice
            self.article_chosen = True
            self.title = self.articles[self.choice_index]

    def wiki_load_text_without_header(self):
        if (self.article_chosen != True):
            return "error no chosen article to be loaded from article list"
        
        
        title = self.title
        params_load = {
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "explaintext":True,
            "exsectionformat": "wiki",
            "exlimit":"max",
            "format": "json"

        }
        response  = requests.get(URL, headers = self.header, params = params_load)
        response.raise_for_status()
        data = response.json()
        pages = data["query"]["pages"]
        page_id = list(pages.keys())[0] 
        full_text = pages[page_id]["extract"]
        self.fullText = full_text
        return self.fullText
        
    def wiki_load_articles_header(self):
        if self.article_chosen  != True:
            return "error no chosen article to be loaded from article list"
        
        title = self.title
        
        params_header = {
            "action":"parse",
            "page": title,
            "prop": "sections",
            "format":"json"
        }
        response = requests.get(URL, headers = self.header, params = params_header)
        response.raise_for_status()
        data = response.json()
        sections = data["parse"]["sections"]
        headers = [section["line"] for section in sections]
        return headers
       
bot = wikitool()




