from NLU import NLU
from web_scraping import web_scraping
from NLG import NLG

import numpy as np
import random
from googlesearch import search


class DM:
    def __init__(self):

        # Setting the search must be performed inside the specific website
        self.site_url = "https://www.hw.ac.uk"
        self.nlu = NLU()
        self.response = ""
        self.scraped_data = []
        self.def_intent = self.nlu.all_intents()  # all defined intents in the dataset
        self.intent = ""
        self.entities = []
        self.source_site = ""
        self.system_no = 2  # System 2 by default
        self.codewords = ["/end", "/stop", "/start", "/terminate", "/sys3", "/sys1", "/sys2", "/sys 3", "/sys 1", "/sys 2"] # Keywords

    def managing_convo(self, inp=None, data=None, source=None, System_no=2):
        # checking for keyword to start, stop or switch between systems.
        if inp.lower().strip() not in self.codewords:
            self.intent = self.nlu.get_intent(inp)

            all_intents = np.setdiff1d(self.def_intent, ['select course'])  # all intents excluding selecct course

            # checking whether the data is empty or atleast the intent is to start extracting the data for the conversation
            if data != [] or self.intent == "select course":

                # if the intent is to select course, start webscrape the data
                if self.intent == "select course":
                    query = f"{inp} site:\"{self.site_url}\""
                    # print(query)
                    self.source_site = self.web_search(query, 1)
                    self.scraped_data = web_scraping(self.source_site).get_passages()
                    self.response = NLG(all_intents=all_intents, intent='select course').gen_respond()

                # proceeding to NLG if the intent is not "select course"
                elif self.intent in all_intents:
                    nlg = NLG(all_intents=all_intents, data=data, intent=self.intent, entities=self.entities, System_no=System_no, sources= source)
                    self.response = nlg.gen_respond()
                else:
                    self.response = "Sorry the message you've sent is considered to be out of my domain,\nI would be really happy to help you with some other questions."
            else:
                self.response = "Sorry, Can you please tell me what course you are willing to talk about?"

        # If the input is a keyword
        else:
            input_txt = inp.lower().strip()
            form_link = "https://forms.office.com/e/TGax7yfZrc"
            if input_txt == "/end" or input_txt == "/stop":
                self.response = f"\nSession Ended\n\nPlease remember:\nYou have been using the system {self.system_no}\n\nPlease fill the Evaluation form : \n\t\t" + form_link
            elif input_txt == "/start":
                self.response = "Lets get started then,\n What course would you like to talk about now?"
            else:
                self.intent = "switch system"
                system_no = int(input_txt[-1])
                self.switch_sys(system_no)
                self.response = NLG().get_system_info(system_no=system_no)

        return self.response, self.intent

    def web_search(self, query, num_results):
        results = search(query, num=num_results, stop=num_results, pause=2)
        if results is None:
            return "No course found"
        else:
            result_link = list(results)[0]  # Selecting the first result from the list
            # print(result_link)
            return result_link

    # System 0 = Info only, System 1 = Sources only, System 2 = Information + Sources
    def switch_sys(self, System_no): # To store the system number
        self.system_no = System_no

    def get_sys(self):
        return self.system_no
