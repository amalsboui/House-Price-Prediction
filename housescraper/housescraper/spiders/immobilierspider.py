import scrapy
from housescraper.items import HouseItem



class ImmobilierspiderSpider(scrapy.Spider):
    name = "immobilierspider"
    allowed_domains = ["www.immobilier.com.tn"]
    start_urls = ["https://www.immobilier.com.tn/resultat-recherche"]

    def parse(self, response):
        houses = response.css("div.col-12.layout-list a.annonce-card")

        for house in houses:
            house_item = HouseItem()

            house_item["titre" ] = house.css("h3::text").get()
            house_item["prix"] = house.css("div.price span::text").get()
            house_item["surface"] = house.css("ul.amenities li:first-child::text").get()
            house_item["chambres"]= house.css("ul.amenities li.chambres::text").get()
            house_item["ville"] = house.css("small::text").get()
            house_item["type_bien"] = house.css("ul.amenities li:nth-child(2)::text").get()

            yield house_item

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)



