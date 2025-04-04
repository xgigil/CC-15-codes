inventory_dictionary = {}

def menu_system():
    print("===== Inventory Management System =====")
    print("1. Add Item")
    print("2. Remove Item")
    print("3. View Inventory")
    print("4. Exit")

def add_item(inventory_dictionary):
    name = input("Enter item name: ")

    try:
        price = float(input("Enter item price: "))
        quantity = int(input("Enter item quantity: "))

        if price >= 0 and quantity >= 0:
            if name in inventory_dictionary:
                inventory_dictionary[name]['price'] = price
                inventory_dictionary[name]['quantity'] += quantity
                print(f"{name} updated successfully!")
            else:
                inventory_dictionary[name] = {'price': price, 'quantity': quantity}
                print(f"{name} added successfully!")
        else:
            print("Error: Price and Quantity should not be negative")

    except ValueError:
        print("Error: Please enter valid number for Price or integer for Quantity")

def remove_item(inventory_dictionary):
    name = input("Enter name to be removed: ")

    if name in inventory_dictionary:
        del inventory_dictionary[name]
        print(f"{name} removed successfully!")
    else:
        print(f"Error: {name} not found in the inventory")

def view_inventory(inventory_dictionary):
    if not inventory_dictionary:
         print("There are no items in the inventory")
    else:
        for name, details in inventory_dictionary.items():
            price = details['price']
            quantity = details['quantity']
            print("Inventory: ")
            print(f"Item: {name}, Price: ${price}, Quantity: {quantity}")

while True:
    menu_system()
    chosen_input = input("Enter your choice: ")
    if chosen_input == "1":
        add_item(inventory_dictionary)
    elif chosen_input == "2":
        remove_item(inventory_dictionary)
    elif chosen_input == "3":
        view_inventory(inventory_dictionary)
    elif chosen_input == "4":
        print("Exiting program...")
        break
    else:
        print("Invalid input. Please select option from 1-4")