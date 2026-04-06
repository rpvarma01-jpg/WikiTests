
import re 

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/w/api.php"




class wikitool: ############IMPORTANT BUG!! NOTES, REFRENCES, OR EXTERNAL LINKS HAVE GLITCHES WHEN LOADED AS SECTIONAL TEXT.
    def __init__(self):
        
         
        self.header = {
        "User-Agent": 'SchoolProject-COMPSCI/1.0 (High School Project; Fairveiw High School; mailto: rpvarma01@bvsd.org)'
        }
        self.articles = []
        self.choice_index = 0
        self.title = ""
        self.article_chosen = False
        self.fullText = ""
        self.headersOfArticle = [];
        self.nestedHeadersOfArticle = [];
    
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
            "explaintext":"1",
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
        nested_headers = []

        for i in range(len(sections) - 1):
            current = sections[i]
            next = sections[i + 1]
            if current["level"] == "2" and next["level"] == "3":
                nested_headers.append(current["line"])
        
        
        self.headersOfArticle = headers
        self.nestedHeadersOfArticle = nested_headers
        return self.headersOfArticle, self.nestedHeadersOfArticle
    
    def wiki_load_section_text(self, section_index): ##returns text. but, sometimes can return text off to the side in like a table and insert it into the text. I have tried to remove this but it is not perfect. I have also tried to remove the references but sometimes they are still there. I have also tried to remove the edit section but sometimes it is still there. I have also tried to remove the navbox but sometimes it is still there. I have also tried to remove the infobox but sometimes it is still there. I have also tried to remove the thumb but sometimes it is still there. I have also tried to remove the extiw but sometimes it is still there. I have also tried to remove the reference but sometimes it is still there. I have also tried to remove the table but sometimes it is still there.
        if self.article_chosen != True:
            return "error no chosen article to be loaded from article list"
        
        title = self.title
        params_section = {
            "action":"parse",
            "page": title,
            "prop": "text",
            "section": section_index,   
            "format":"json"
        }
        response = requests.get(URL, headers = self.header, params = params_section)
        response.raise_for_status()
        data = response.json()
        raw_data = data["parse"]["text"]["*"]
       
        soup = BeautifulSoup(raw_data, "html.parser")

        section_title = self.headersOfArticle[section_index - 1].lower()

        if "notes" not in section_title:
            for i in soup.select((".thumb, .infobox, .reference, .extiw, table, .navbox, .mw-editsection")):
                i.decompose()
        
        for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            header.decompose()

        readable_data = soup.get_text()
        readable_data = readable_data.strip()
        
        if "notes" not in section_title:
            readable_data = re.sub(r'\^', 'Refrences used for this specific section: \n', readable_data, count =1)
            readable_data = re.sub(r'Main article:', 'The actual article where this section is found is called: ', readable_data)
            readable_data = re.sub(r'Main articles:', 'The actual articles where this section is found are called: ', readable_data)
        return readable_data

    def wiki_get_section_index_by_name(self, section_name):
        if self.article_chosen != True:
            return "error no chosen article to be loaded from article list"
        
        if self.headersOfArticle == []:
            return "error no loaded headers of article to search through for section index"
        
        for i in range(len(self.headersOfArticle)):
            if self.headersOfArticle[i].lower() == section_name.lower():
                return i + 1
        
        return "error no section with that name found in article headers"
    
def pretty_print(text, limit):
    
    if isinstance(text, str):
        print(text)
        return
    
    if (limit == "max"):
        limit = len(text)
            
    for i in range(0, limit):
        print(str(i) + ": " + text[i])
        
    print("\n")



if __name__ == "__main__":
    bot = wikitool()
    
    pretty_print(bot.wiki_search("monkey"), 10)

    title = input("Enter the index of the article you want to load: ")

    bot.wiki_choose(int(title))

    bot.wiki_load_articles_header()

    section_index = bot.wiki_get_section_index_by_name("Notes")
    print(section_index)
    print(bot.wiki_load_section_text(section_index))




