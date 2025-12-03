"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice

    print("\n" + "=" * 20)
    print("      MAIN MENU")
    print("=" * 20)
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    while True:
        choice = input("Select an option (1-3): ")
        if choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    print("\n--- NEW GAME ---")
    name = input("Enter your character's name: ").strip()
    if not name:
        print("Name cannot be empty. Going back to main menu.")
        return
    
    print(f"Valid classes are: {', '.join(character_manager.valid_class)}")
    char_class = input("Choose your class: ").strip().capitalize()
    
    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"\nCharacter {name} the {char_class} has been created!")

        save_game()
        print(f"Game saved. {name}, ENGAGE!")

        game_loop()

    except InvalidCharacterClassError as e:
        print(f"Error: {e}")
        print("Returning to main menu.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    global current_character
    print("\n--- LOAD GAME ---")
    saved_chars = character_manager.list_saved_characters()
    
    if not saved_chars:
        print("No saved games found.")
        return
        
    print("Available characters:")
    for i, name in enumerate(saved_chars, 1):
        print(f"{i}. {name}")
        
    choice = input("Enter the name of the character to load: ").strip()
    try:
        current_character = character_manager.load_character(choice)
        print(f"\nWelcome back, {current_character['name']}!")
        
        game_loop()
    except (CharacterNotFoundError, SaveFileCorruptedError, InvalidSaveDataError) as e:
        # 4. CATCH exceptions
        print(f"Error loading game: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        if current_character and character_manager.is_character_dead(current_character):
            current_character, game_running = handle_character_death(current_character)
            continue

        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("\nGame saved. Goodbye!")
            game_running = False
        
        if game_running:
            try:
                # We auto-save the character after every action
                character_manager.save_character(current_character)
            except IOError as e:
                print(f"!! CRITICAL: Failed to auto-save game: {e} !!")

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("\n" + "=" * 20)
    print("      GAME MENU")
    print("=" * 20)
    print(f"Name: {current_character['name']} | Level: {current_character['level']}")
    print(f"HP: {current_character['health']}/{current_character['max_health']} | Gold: {current_character['gold']}")
    print("-" * 20)
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battle)")
    print("5. Shop")
    print("6. Save and Quit to Main Menu")
    
    while True:
        choice = input("Select an option (1-6): ")
        if choice.isdigit() and 1 <= int(choice) <= 6:
            return int(choice)
        else:
            print("Invalid choice. Please enter a number 1-6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    print("\n--- CHARACTER STATS ---")
    print(f"  Name: {current_character['name']}")
    print(f"  Class: {current_character['class']}")
    print(f"  Level: {current_character['level']}")
    print(f"  Health: {current_character['health']}/{current_character['max_health']}")
    print(f"  XP: {current_character['experience']}")
    print(f"  Strength: {current_character['strength']}")
    print(f"  Magic: {current_character['magic']}")
    print(f"  Gold: {current_character['gold']}")

    quest_handler.display_character_quest_progress(current_character, all_quests)
    
    input("\nPress Enter to continue...")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler

    while True:
        print("\n--- INVENTORY ---")
        inventory_system.display_inventory(current_character, all_items)
        
        print("\n(U)se, (E)quip, (S)ell, (B)ack")
        choice = input("Choose an action: ").strip().upper()

        if choice == 'B':
            break
        elif choice not in ['U', 'E', 'S']:
            print("Invalid choice.")
            continue
            
        try:
            item_id = input("Enter the Item ID to use/equip/sell: ").strip()
            if item_id not in all_items:
                print("That is not a valid item ID.")
                continue
                
            item_data = all_items[item_id]

            if choice == 'U':
                result = inventory_system.use_item(current_character, item_id, item_data)
                print(result)
            
            elif choice == 'S':
                gold = inventory_system.sell_item(current_character, item_id, item_data)
                print(f"You sold {item_data['name']} for {gold} gold.")
                
            elif choice == 'E':
                if item_data['type'] == 'weapon':
                    result = inventory_system.equip_weapon(current_character, item_id, item_data)
                    print(result)
                elif item_data['type'] == 'armor':
                    result = inventory_system.equip_armor(current_character, item_id, item_data)
                    print(result)
                else:
                    print("You can only equip 'weapon' or 'armor' type items.")

        except (ItemNotFoundError, InvalidItemTypeError, InsufficientResourcesError, InventoryFullError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        input("\nPress Enter to continue...")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

