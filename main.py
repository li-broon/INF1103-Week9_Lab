import abc
from abc import abstractmethod
import json
import os

class CanBeShipped(abc.ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Product(abc.ABC):
    def __init__(self, productId, name, price, stock):
        self._productid = productId
        self.name = name
        self._price = price
        self._stock = stock

    def update_stock(self, quantity:int):
        self._stock = quantity if quantity >= 0 else 0

    def display_information(self):
        print(f"Product Name: {self.name}\n")
        print(f"Product ID: {self._productid}\n")
        print(f"Product Price: {self._price}\n")
        print(f"Product Stock Quantity: {self._stock}\n")

    def to_dict(self):
        return {
            "product_id": self._productid,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }
    @abstractmethod
    def get_fulfilment_info(self):
        pass

class Inventory:
    def __init__(self,products):
        self.productslist = products

    def add_product(self, product):
        self.productslist.append(product)

    def search_product(self, target_name):
        for product in self.productslist:
            if product.name.lower() == target_name.lower():
                return product
        return None

    def display_all(self):
        for product in self.productslist:
            product.display_information()

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, productId, name, price, stock, weight):
        super().__init__(productId, name, price, stock)
        self.weight = weight  

    def get_fulfilment_info(self):
        return "This product requires physical shipping."
    def display_information(self):
        print("---------------------------\n")
        super().display_information()
        print(f"Product Weight:{self.weight}")
        print("---------------------------\n")
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.weight
        return data

    def calculate_shipping_cost(self):
        return 5.0 + (2.0 * self.weight)



class DigitalProduct(Product):
    def __init__(self, productId, name, price, stock, download_size):
        super().__init__(productId, name, price, stock)
        self.download_size = download_size

    def get_fulfilment_info(self):
        return "This product is delivered to you digitally."
    def display_information(self):
            print("---------------------------\n")
            super().display_information()
            print(f"Download Size:{self.download_size}")
            print("---------------------------\n")  
    def to_dict(self):
            data = super().to_dict()
            data["type"] = "digital"
            data["download_size"] = self.download_size
            return data

def save_inventory_to_json(inventoryList):
    dict_inventory = []

    for product in inventoryList:
        dict_inventory.append(product.to_dict())

    with open("inventory.json","w") as file:
         json.dump(dict_inventory, file, indent=4)

def load_inventory_from_json():
    if not os.path.exists("inventory.json"):
        return [] 
    
    with open("inventory.json", "r") as file:
        try:
            data = json.load(file)
            inventorylist = []

            for item_object in data:
                if item_object["type"] == "physical":
                    existing_product = PhysicalProduct(item_object["product_id"], item_object["name"], item_object["price"], item_object["stock"], item_object["weight"])
                else:
                    existing_product = DigitalProduct(item_object["product_id"], item_object["name"], item_object["price"], item_object["stock"], item_object["download_size"])

                inventorylist.append(existing_product)

            return inventorylist
        except json.JSONDecodeError:
            return []

def main():
    # 1. Load initial data and create Inventory object
    loaded_products = load_inventory_from_json()
    inventory = Inventory(loaded_products)

    while True:
        print("\n=== Inventory Management System ===")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            inventory.display_all()

        elif choice == '2':
            print("\nSelect Product Type:")
            print("1. Physical Product")
            print("2. Digital Product")
            prod_type = input("Enter choice (1 or 2): ")

            if prod_type not in ['1', '2']:
                print("Invalid product type selected.")
                continue

            # Main program handles input for shared attributes
            p_id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock Quantity: "))
            
            # Branch based on the user's choice to get specific attributes
            if prod_type == '1':
                weight = float(input("Enter Weight (in kg): "))
                new_product = PhysicalProduct(p_id, name, price, stock, weight)
            elif prod_type == '2':
                dl_size = float(input("Enter Download Size (in MB): "))
                new_product = DigitalProduct(p_id, name, price, stock, dl_size)

            inventory.add_product(new_product)
            print(f"Product '{name}' added successfully.")

        elif choice == '3':
            target = input("Enter the name of the product to update: ")
            # Menu interacts with Inventory to find the object
            product = inventory.search_product(target)
            
            if product:
                new_qty = int(input(f"Enter new stock quantity for {product.name}: "))
                # Product object manages its own state
                product.update_stock(new_qty)
                print("Stock updated successfully.")
            else:
                print("Product not found.")

        elif choice == '4':
            target = input("Enter the name of the product to search: ")
            product = inventory.search_product(target)
            
            if product:
                product.display_information()
            else:
                print("Product not found.")

        elif choice == '5':
            # Pass the list of Product objects to your save function
            save_inventory_to_json(inventory.productslist)
            print("Inventory saved successfully to inventory.json.")

        elif choice == '6':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()