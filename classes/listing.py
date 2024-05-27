class Listing:
    def __init__(self, title, price, description):
        self.title = title
        self.price = price
        self.description = description

    def __str__(self) -> str:
        return f"Title: {self.title}\nPrice: {self.price}\nDescription: {self.description}"
