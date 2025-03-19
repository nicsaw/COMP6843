from bs4 import BeautifulSoup
import re

HTML_FILENAME = "challenges.html"

class Challenge:
    def __init__(self, category: str, name: str, points: int, stars: int, tags: list[str]):
        self.category = category
        self.name = name
        self.points = points
        self.stars = stars
        self.tags = tags

    def to_dict(self):
        return {
            "category": self.category,
            "name": self.name,
            "value": self.points,
            "stars": self.stars,
            "tags": self.tags,
        }

    def __str__(self):
        return f"{self.category} - {self.name}\n{self.points} points{f" | {'⭑' * self.stars}" if self.stars >= 1 else ''}{f" | Tags: {self.tags}" if self.tags else ''}"

class ChallengeBoardScraper:
    def __init__(self, html_filename: str = HTML_FILENAME):
        with open(html_filename) as f:
            self.soup = BeautifulSoup(f, "html.parser")

    def is_hidden(element):
        return "display: none" in element.get("style", "").lower()

    def scrape(self):
        challenges = []

        for category_div in self.soup.find_all("div", class_="pt-5"):
            if category_div.find_parent("template"): continue

            category = category_div.find("h3").get_text(strip=True)

            for button_element in category_div.find_all("button", class_="challenge-button"):
                if button_element.find_parent("template"): continue

                inner_div = button_element.find("div", class_="challenge-inner")
                name = inner_div.find('p').get_text(strip=True)

                values_text = inner_div.find("span").get_text(strip=True)
                points = int(re.search(r"\d+", values_text).group())
                stars = values_text.count('⭑')

                tags = []
                for cls, flag in (("challenge-intro", "Intro"), ("challenge-reportable", "Reportable")):
                    tag = button_element.find("span", class_=cls)
                    if tag and not self.is_hidden(tag):
                        tags.append(flag)

                challenges.append(Challenge(category, name, points, stars, tags))

        return challenges

if __name__ == "__main__":
    scraper = ChallengeBoardScraper()
    challenges = scraper.scrape()
    for challenge in challenges:
        print(challenge)
