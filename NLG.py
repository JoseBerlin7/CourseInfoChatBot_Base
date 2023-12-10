import random
import numpy as np

from rank_bm25 import BM25Okapi


class NLG:
    def __init__(self, all_intents=None, data=None, intent=None, entities=None, sources=None, System_no=2):
        self.all_intent = all_intents
        self.data = data
        self.entities = entities
        self.intent = intent
        self.sources = sources  # Sources of the content [i.e., the site from which the content will be scraped]
        self.sys_no = System_no  # System number [i.e, 0= information only, 1 = sources only, 2 = Information +
        # Sources] Here the default system always provides Information + Sources

    def raw_ans(self, intent):

        # Extract the heading from the passages
        passages = [passage["heading"].lower().split() for passage in self.data]

        bm25 = BM25Okapi(passages)

        query_tokens = intent.lower().split()

        # Get the BM25 scores for each passage
        bm25_scores = bm25.get_scores(query_tokens)

        # converting bm25 scores for all heading
        bm25_scr_np = np.array(bm25_scores)

        # Find the index of the most relevant passage
        most_rel_index = np.argmax(bm25_scr_np)

        # Narrowing down to passage
        most_rel_passage = self.data[most_rel_index]

        ans = f"{most_rel_passage['content'].strip()}"

        return ans

    def gen_respond(self):
        if self.intent == 'select course':
            x = [
                "I'm here to offer information about the 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', 'contacting faculty members'. What aspect of the course interests you?",
                "Feel free to ask about any of the following topics: 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', 'contacting faculty members'. How can I assist you with the course details?",
                "If you're curious about 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', 'contacting faculty members', just let me know. What information would you like about the course?",
                "I have information on 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', 'contacting faculty members'. Is there something specific you'd like to know about the course?",
                "Any questions you have about 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', 'contacting faculty members'—I've got answers. What's on your mind regarding the course?",
                "You can inquire about 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', 'contacting faculty members'. What would you like me to explain about the course?",
                "Whether it's about 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', or 'contacting faculty members', I'm here to help. What specifics do you want to know regarding the course?",
                "I'm equipped to provide insights on 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', 'contacting faculty members'. What area of the course would you like more information about?",
                "Wondering about 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', or 'contacting faculty members'? Just let me know which aspect of the course you're interested in.",
                "I've got all the details on 'course delivery', 'course location', 'duration of the course', 'overview of the program', 'course contents', 'course entry requirements', 'program fees', 'how to apply', 'contacting faculty members'. What aspect of the course are you curious about?"
            ]
            output = random.choice(x)
        elif self.intent in self.all_intent:
            ans = ""
            # Generating Answers based on the system we are working in
            if self.sys_no == 1:
                ans = self.raw_ans(self.intent)
            elif self.sys_no == 3:
                ans = f"You will be able to find the answer in the following site: \n\n {self.sources}"
            else:
                ans = f"{self.raw_ans(self.intent)}\n\nSOURCES:\n\t{self.sources}"
            output = ans
        else:
            output = "Sorry, The enquiry is considered out of the scope for my domain.\n I would be glad to help you with anything else."

        return output

    def get_system_info(self, system_no):
        info = ""
        if system_no == 1:
            info = "Information Only"
        elif system_no == 3:
            info = "Sources only"
        else:
            info = "Information with sources"

        info = f"System has been switched to {info}, [i.e., System {system_no}]"

        return info
