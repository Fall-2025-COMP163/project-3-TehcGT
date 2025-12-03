"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Tehcubelleh Keamu

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

import character_manager
from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(
            f"Cannot add {item_id}: Inventory is full "
            f"({len(character['inventory'])}/{MAX_INVENTORY_SIZE})."
        )
    
    character['inventory'].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Cannot remove: {item_id} not found in inventory.")
        
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    return item_id in character['inventory']

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    return MAX_INVENTORY_SIZE - len(character['inventory'])

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    removed_items = character['inventory'].copy()
    character['inventory'].clear()
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Cannot use: {item_id} not in inventory.")
        
    if item_data['type'] != 'consumable':
        raise InvalidItemTypeError(f"Cannot 'use' item of type: {item_data['type']}.")
        
    try:
        stat_name, value = parse_item_effect(item_data['effect'])
        
        apply_stat_effect(character, stat_name, value)

        remove_item_from_inventory(character, item_id)
        
        return f"Used {item_data.get('name', item_id)}. {stat_name} increased by {value}."
        
    except ValueError as e:
        raise InvalidItemTypeError(f"Item {item_id} has invalid effect data: {e}")
    except ItemNotFoundError:
        return "Error: Item was used but could not be removed."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Cannot equip: {item_id} not in inventory.")
        
    if item_data['type'] != 'weapon':
        raise InvalidItemTypeError(f"Cannot equip item of type: {item_data['type']}.")
    
    unequipped_msg = ""
    if character.get('equipped_weapon'):
        try:
            old_item_id = unequip_weapon(character)
            unequipped_msg = f"Unequipped {old_item_id}. "
        except InventoryFullError:
            return "Cannot equip new weapon: Inventory is full!"
    try:
        stat_name, value = parse_item_effect(item_data['effect'])
        apply_stat_effect(character, stat_name, value)

        character['equipped_weapon'] = {'id':item_id, 'effect': item_data['effect']}
        
        remove_item_from_inventory(character, item_id)
        
        return f"{unequipped_msg}Equipped {item_data.get('name', item_id)}."
        
    except ValueError as e:
        return f"Error equipping {item_id}: Invalid effect data. {e}"

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Cannot equip: {item_id} not in inventory.")
        
    if item_data['type'] != 'armor':
        raise InvalidItemTypeError(f"Cannot equip item of type: {item_data['type']}.")

    unequipped_msg = ""
    if character.get('equipped_armor'):
        try:
            old_item_id = unequip_armor(character)
            unequipped_msg = f"Unequipped {old_item_id}. "
        except InventoryFullError:
            return "Cannot equip new armor: Inventory is full!"
            
    try:
        stat_name, value = parse_item_effect(item_data['effect'])
        apply_stat_effect(character, stat_name, value)
        
        character['equipped_armor'] = {'id': item_id, 'effect': item_data['effect']}
        remove_item_from_inventory(character, item_id)
        
        return f"{unequipped_msg}Equipped {item_data.get('name', item_id)}."
        
    except ValueError as e:
        return f"Error equipping {item_id}: Invalid effect data. {e}"

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    if not character.get('equipped_weapon'):
        return None # Nothing was equipped
    
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot unequip weapon: Inventory is full.")
    
    equipped = character['equipped_weapon']
    item_id = equipped['id']
    effect_string = equipped['effect']

    try:
        stat_name, value = parse_item_effect(effect_string)
        apply_stat_effect(character, stat_name, -value)
    except ValueError:
        print(f"Warning: Could not parse effect for equipped item {item_id}.")
        
    add_item_to_inventory(character, item_id)
    
    character['equipped_weapon'] = None
    
    return item_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    if not character.get('equipped_armor'):
        return None # Nothing was equipped

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot unequip armor: Inventory is full.")

    equipped = character['equipped_armor']
    item_id = equipped['id']
    effect_string = equipped['effect']
    
    try:
        stat_name, value = parse_item_effect(effect_string)
        apply_stat_effect(character, stat_name, -value) # Apply negative
    except ValueError:
        print(f"Warning: Could not parse effect for equipped item {item_id}.")
        
    add_item_to_inventory(character, item_id)
    character['equipped_armor'] = None
    
    return item_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    cost = item_data['cost']
    if character['gold'] < cost:
        raise InsufficientResourcesError(
            f"Cannot buy {item_id}: Costs {cost} gold, "
            f"you only have {character['gold']}."
        )
    add_item_to_inventory(character, item_id)

    if len(character['inventory']) >= 20:
        raise InventoryFullError("Inventory is full, cannot purchase item.")

    character['gold'] -= cost


    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    remove_item_from_inventory(character, item_id)
    
    sell_price = item_data['cost'] // 2
    character['gold'] += sell_price
    
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    try:
        parts = effect_string.split(':')
        stat_name = parts[0]
        value = int(parts[1])
        return (stat_name, value)
    except (IndexError, ValueError):
        # Raise an error that the calling function can catch
        raise ValueError(f"Invalid effect string format: '{effect_string}'")

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    if stat_name == 'health':

        character_manager.heal_character(character, value)
    
    elif stat_name == 'max_health':
        character['max_health'] += value
        character_manager.heal_character(character, value)
        
    elif stat_name == 'strength':
        character['strength'] += value
        
    elif stat_name == 'magic':
        character['magic'] += value
        
    else:
        print(f"Warning: Invalid stat name '{stat_name}' in apply_stat_effect")

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    print("--- INVENTORY ---")
    
    # Check if inventory is empty
    if not character['inventory']:
        print(" (Empty)")
        return

    # 1. Count the items
    item_counts = {}
    for item_id in character['inventory']:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1
        
    # 2. Prepare a list of items to print so we can SORT them
    items_to_print = []
    
    for item_id, quantity in item_counts.items():
        # Get item info, default to empty dict if missing
        item_info = item_data_dict.get(item_id)
        
        if item_info:
            display_name = item_info.get('name', item_id)
            items_to_print.append((display_name, quantity))
        else:
            # Fallback for unknown items
            display_name = f"{item_id} [Unknown Item]"
            items_to_print.append((display_name, quantity))

    # 3. Sort the list alphabetically by name
    # This is usually what fixes test case failures!
    items_to_print.sort(key=lambda x: x[0])

    # 4. Print the sorted items
    for name, quantity in items_to_print:
        print(f"- {name} (x{quantity})")
    
    # Note: Ensure you have the 'get_inventory_space_remaining' function imported or defined
    # print(f"Space remaining: {get_inventory_space_remaining(character)}")
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

