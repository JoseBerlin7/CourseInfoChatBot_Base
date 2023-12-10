import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import html


class web_scraping:
    def __init__(self, site):
        self.site_link = site
        self.raw_content = self.get_raw_site_contents()

    def get_raw_site_contents(self):
        # setting up a user agent in your requests to make it appear as a regular browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        raw_contents = requests.get(url=self.site_link, headers=headers)

        return raw_contents.text

    def get_abs_url(self, redirect_link):
        # Base URL of the website
        base_url = "https://www.hw.ac.uk"

        # Relative URL from our HTML snippet
        relative_url = redirect_link

        # Decode HTML entities in the relative URL
        relative_url = html.unescape(relative_url)

        # Combine the base URL and relative URL to create the absolute URL
        absolute_url = urljoin(base_url, relative_url)

        return absolute_url

    # Here is where the raw contents of the website will be processed into passages
    def get_passages(self):
        soup = BeautifulSoup(self.raw_content, "html.parser")

        # Finding all headings and their contents
        all_headings = ["h1", "h2", "h3", "h4", "h5", "h6"]
        headings = soup.find_all(all_headings)
        passages = []  # Just a Container to store all passages

        for heading in headings:

            # finding all siblings until the next heading
            sib = ['p', 'ul', 'ol', 'table', 'dl']  # all the siblings we should consider

            paragraph = heading.find_next_sibling(sib)
            passage_txt = ""

            while paragraph and paragraph.name not in headings:

                # Exxtracting data from tables
                if paragraph.name == 'table':
                    table = paragraph
                    caption = table.find_all('caption')
                    for cap in caption:
                        passage_txt += cap.get_text() + ":\n"
                    rows = table.find_all("tr")
                    for row in rows:
                        cols = row.find_all(["th", "td"])
                        row_txt = ""
                        for col in cols:
                            row_txt += col.get_text().strip() + ": "
                        passage_txt += row_txt + "\n"
                    passage_txt += "\n"
                # Extracting data from description list
                elif paragraph.name == "dl":
                    dts = paragraph.find_all("dt")
                    for dt in dts:
                        dd = dt.find_next_sibling("dd")
                        passage_txt += dt.get_text().strip() + ": " + dd.get_text().strip() + "\n"
                elif paragraph.name == 'ul' or paragraph.name == 'ol':
                    items = paragraph.find_all('li')
                    passage_txt += "\n".join([f"\t\t⁂ {item.get_text()}" for item in items])
                    passage_txt += "\n"
                else:
                    passage_txt += paragraph.get_text().strip() + "\n"
                paragraph = paragraph.find_next_sibling(sib)

            heading_txt = heading.get_text().strip().lower()
            if passage_txt != "" and heading_txt != "contact" and heading_txt != "apply":
                passages.append({"heading": heading_txt, "content": f"{heading_txt.upper()}:\n{passage_txt}"})

        # Initialize variables for the links
        apply_link = None
        contact = None

        all_anchor_tags = soup.find_all('a')

        # Iterate through anchor tags and check their text content
        for anchor_tag in all_anchor_tags:
            if "Find out how to apply" in anchor_tag.get_text() or "Apply now" in anchor_tag.get_text():
                apply_link = anchor_tag['href']
            elif "Contact us" in anchor_tag.get_text():
                contact = anchor_tag['href']

        # Check if the links were found
        if apply_link:
            passages.append({"heading": "Apply",
                             'content': f"\nFollow the provided link below to apply for the course : \n{self.get_abs_url(apply_link)}"})
        else:
            passages.append(
                {"heading": "Apply",
                 "content": "\nHow to Apply for the course : \nSorry, \nthe requested details couldn't be found"})

        if contact:
            passages.append({"heading": "Contact", 'content': f"\nContact for the course : \n{contact}"})
        else:
            passages.append(
                {"heading": "Contact",
                 "content": "\nContact for the course : \nSorry, \nthe requested details couldn't be found"})

        content = ""

        for passage in passages:
            content += passage['content'] + "\n\nEnd of passage\n\n"

        return passages