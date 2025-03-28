class CharacterInventory:
    def __init__(self):
        # Initialize characters list and dictionary for character data
        self.characters = []
        self.character_dict = {}

    def add_character(self, name, level, inventory):
        # Add a new character if not already in the dictionary
        if name in self.character_dict:
            print(f"\n'{name}' already exists")
            return
        inventory_tuple = tuple(inventory)  # Convert inventory list to tuple
        character_data = {"name": name, "level": level, "inventory": inventory_tuple}
        self.characters.append(character_data)  # Add character to list
        self.character_dict[name] = character_data  # Add character to dictionary
        print(f"\nCharacter added: {name} (Level {level}) - Inventory: {inventory_tuple}")

    def display_characters(self):
        # Display all characters and their details
        if not self.characters:
            print("\nThere are no characters to be displayed")
            return
        print("\nCharacters and Their Inventories:")
        for num, char in enumerate(self.characters, start=1):
            print(f"{num}. {char['name']} Level {char['level']} - Inventory: {char['inventory']}")

    def get_character(self, name):
        # Retrieve and display character details by name
        if name in self.character_dict:
            char = self.character_dict[name]
            print(f"\nCharacter found: {char['name']} Level {char['level']} - Inventory: {char['inventory']}")
        else:
            print("\nCharacter not found")

    def add_item(self, name, item):
        # Add an item to a character's inventory
        if name in self.character_dict:
            character_data = self.character_dict[name]
            new_inventory = character_data['inventory'] + (item,)  # Update inventory
            character_data['inventory'] = new_inventory
            print(f"\n{name}'s inventory updated: {new_inventory}")
        else:
            print("\nCharacter not found")

    def remove_character(self, name):
        # Remove a character from the game
        character_removed = self.character_dict.pop(name, None)
        if character_removed:
            self.characters = [char for char in self.characters if char["name"] != name]
            print(f"\n{name} has been removed from the game.")
        else:
            print("\nCharacter not found.")

    def search_item(self, name, item):
        # Search for an item in a character's inventory
        character_searched = self.character_dict.get(name)
        if character_searched:
            if item in character_searched["inventory"]:
                print(f"\n{name} has the item: {item}")
            else:
                print(f"\n{name} does not have this item")
        else:
            print("\nCharacter not found")

    def character_with_the_most_items(self):
        # Find and display the character with the most items
        if not self.characters:
            print("No characters available")
            return
        most_items_by_character = max(self.characters, key=lambda char: len(char["inventory"]))
        print(f"\n{most_items_by_character['name']} (Level {most_items_by_character['level']}) - Inventory: {most_items_by_character['inventory']}")



# Test Samples
characterList = CharacterInventory() # Creates an instance of the CharacterInventory class

characterList.display_characters() # Demonstrates how the code handles error if this method is called when there are no characters to display

characterList.add_character("Alice", 10, ["Sword", "Shield"]) # Adds a character named Alice
characterList.add_character("Bea", 100, ["Bow", "Arrow"]) # Adds a character named Bea
characterList.add_character("Oliver", 9, ["Wand", "Robe"]) # Adds a character named Oliver
characterList.add_character("Alice", 10, ["Sword"]) # Demonstrate how the code handles name duplication errors

characterList.display_characters() # Displays the list of characters

characterList.get_character("Alice") # Searches for a character using their name

characterList.add_item("Bea", "Swift Potion") # Adds Swift Potion in Bea's inventory
characterList.add_item("Oliver", "Healing Potion") # Adds Healing Potion in Oliver's inventory
characterList.display_characters() # Demonstrates that the display matches the changes

characterList.remove_character("Oliver") # Removes the character Oliver
characterList.get_character("Oliver") # Demonstrates that Oliver can not be searched due to removal from the game
characterList.display_characters() # Display matches the changes

characterList.search_item("Alice","Sword") # Searches Sword in Alice's inventory
characterList.search_item("Alice","Bow") # Demonstrates how the code deals when an item is not in the character's inventory

characterList.character_with_the_most_items() # Shows the character with the most items in their inventory