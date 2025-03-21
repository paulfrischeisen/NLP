import scrapy


class ChefkochSpider(scrapy.Spider):
    name = "chefkoch"
    allowed_domains = ["www.chefkoch.de"]
    start_urls = ["https://www.chefkoch.de/rezepte/1524131257670024/Gestovte-gruene-Bohnen.html"]

    def parse(self, response):
        # Rezepte-Links sammeln
        for recipe in response.css("a.gs-title"):   # CSS-Selector für Rezeptlinks
            recipe_url = response.urljoin(recipe.attrib["href"])
            yield scrapy.Request(recipe_url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        title = response.css("h1::text").get().strip()
        ingredients = response.css(".ingredient ::text").getall()    # Zutaten extrahieren
        instructions = response.css(".ds-recipe-meta-recipe p::text").getall()      # Zubereitung

        yield {
            "title": title,
            "ingredients": [i.strip() for i in ingredients if i.strip()],
            "instructions": " ".join(i.strip() for i in instructions if i.strip())
        }
