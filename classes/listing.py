class Listing:
    def __init__(self, link, title, price, description, img):
        self.link = link
        self.title = title
        self.price = price
        self.description = description
        self.img = img

    def __str__(self) -> str:
        return f"Title: {self.title}\nPrice: {self.price}\nDescription: {self.description}"
