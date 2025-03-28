from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, name, price, stock):
        self.name = name
        self._price = 0
        self._stock = 0
        self.price = price
        self.stock = stock

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        try:
            if new_price > 0:
                self._price = new_price
            else:
                raise ValueError("Price must be positive.")
        except ValueError as e:
            print(f"Error: {e}")

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, quantity):
        try:
            if quantity >= 0:
                self._stock = quantity
            else:
                raise ValueError("Stock must not be negative.")
        except ValueError as e:
            print(f"Error: {e}")

    @abstractmethod
    def apply_discount(self):
        pass

    def sell(self, quantity):
        if quantity <= 0:
            print("Error: Quantity to sell must be positive.")
        elif quantity <= self.stock:
            self.stock -= quantity
            print(f"Sold {quantity} units of {self.name}. Remaining stock: {self.stock}")
        else:
            print(f"Error: Insufficient stock! Available: {self.stock}")

    def update_product(self,new_price, new_stock):
        self.price = new_price
        self.stock = new_stock
        print(f"Updated {self.name}: Price - ${self.price}, Stock - {self.stock}")

    def display_info(self):
        print(f"{self.name}: Price - ${self.price}, Stock - {self.stock}")


class Electronics(Product):
    def __init__(self, name, price, stock, warranty_years):
        super().__init__(name, price, stock)
        self.warranty_years = warranty_years

    def apply_discount(self):
        self.price *=0.90

    def display_info(self):
        print(f"{self.name} (Electronics): ${self.price}, Stock: {self.stock}, Warranty: {self.warranty_years} years")


class Grocery(Product):
    def __init__(self, name, price, stock, perishable):
        super().__init__(name, price, stock)
        self.perishable = perishable

    def apply_discount(self):
        if self.perishable:
            self.price *= 0.80

    def display_info(self):
        status = "Perishable" if self.perishable else "Non-Perishable"
        print(f"{self.name} (Grocery): ${self.price}, Stock: {self.stock}, Type: {status}")


class Clothing(Product):
    def __init__(self, name, price, stock, size):
        super().__init__(name, price, stock)
        self.size = size

    def apply_discount(self):
        if self.stock > 50:
            self.price *= 0.85

    def display_info(self):
        print(f"{self.name} (Clothing): ${self.price}, Stock: {self.stock}, Size: {self.size}")


def show_product_details(product):
    product.display_info()


apple = Grocery("Apple", 2, 100, True)
tshirt = Clothing("T-Shirt", 25, 60, "L")
laptop = Electronics("Laptop", 1200, -5, 2)

print("\n---Before Discount---")
show_product_details(apple)
show_product_details(tshirt)

apple.apply_discount()
tshirt.apply_discount()

print("\n---After Discount---")
show_product_details(apple)
show_product_details(tshirt)

apple.sell(10)
tshirt.sell(-5)
tshirt.sell(100)
tshirt.sell(5)