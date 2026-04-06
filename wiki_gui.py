import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from wiki  import wikitool



class WikiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wiki Tool")
        self.total_article_text = ""
        self.total_section_text = ""
        self.bot = wikitool()
        # MAIN FRAMES
        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0, padx=10, pady=10)

        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=1, padx=10, pady=10)

        bottom_frame = tk.Frame(root)
        bottom_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # -------------------
        # ARTICLE SEARCH
        # -------------------
        tk.Label(left_frame, text="Article Search").grid(row=0, column=0)

        self.search_entry = tk.Entry(left_frame, width=30)
        self.search_entry.grid(row=1, column=0)

        tk.Button(left_frame, text="Search", command=self.search).grid(row=1, column=1)

        # -------------------
        # SECTION LOAD
        # -------------------
        tk.Label(left_frame, text="Section Load").grid(row=2, column=0)

        self.section_entry = tk.Entry(left_frame, width=30)
        self.section_entry.grid(row=3, column=0)

        tk.Button(left_frame, text="Load", command=self.load_section).grid(row=3, column=1)

        # -------------------
        # PRINT BUTTONS
        # -------------------
        tk.Button(left_frame, text="Print Article Text", command=self.print_article).grid(row=4, column=0, pady=5)
        tk.Button(left_frame, text="Print Section Text", command=self.print_section).grid(row=5, column=0, pady=5)

        # -------------------
        # STATUS BOX (RIGHT)
        # -------------------
        tk.Label(right_frame, text="Status").pack()

        self.status_label = tk.Label(right_frame, text="Nothing loaded", relief="solid", width=30, height=10)
        self.status_label.pack()

        # -------------------
        # HEADERS DISPLAY
        # -------------------
        self.headers_label = tk.Label(bottom_frame, text="Headers will appear here", wraplength=400)
        self.headers_label.pack()

        # -------------------
        # AI BUTTON
        # -------------------
        tk.Button(bottom_frame, text="Send to AI for Summarization", command=self.send_to_ai).pack(pady=10)

        # DATA STORAGE (connect to your class later)
        self.article_text = ""
        self.section_text = ""

    # -------------------
    # FUNCTIONS
    # -------------------

    def search(self):
        query = self.search_entry.get()
        self.status_label.config(text=f"Searched for: {query}")
        

        # hook your wikitool here
        # results = bot.wiki_search(query)

        self.headers_label.config(text="Headers: (example)\nHistory\nSociety\nCulture")

    def load_section(self):
        section = self.section_entry.get()
        self.status_label.config(text=f"Loaded section: {section}")

        # hook your wikitool here
        # index = bot.wiki_get_section_index_by_name(section)
        # self.section_text = bot.wiki_load_section_text(index)

    def print_article(self):
        self.open_popup("Article Text", self.article_text or "No article loaded")

    def print_section(self):
        self.open_popup("Section Text", self.section_text or "No section loaded")

    def send_to_ai(self):
        text = self.section_text or "No data"
        self.open_popup("AI Summary", f"(Pretend AI summary of)\n\n{text}")

    def open_popup(self, title, content):
        popup = tk.Toplevel(self.root)
        popup.title(title)

        text_box = tk.Text(popup, wrap="word")
        text_box.insert("1.0", content)
        text_box.pack(expand=True, fill="both")
        scrollbar = tk.Scrollbar(popup, command=text_box.yview)
        scrollbar.pack(side="right", fill="y")
        text_box.config(yscrollcommand=scrollbar.set)

# RUN APP
root = tk.Tk()
app = WikiGUI(root)
root.mainloop()