"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

import random
import character_manager
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    if enemy_type == "goblin":
        return {
            'name': 'Goblin', 'health': 50, 'max_health': 50,
            'strength': 8, 'magic': 2, 'xp_reward': 25, 'gold_reward': 10
        }
    elif enemy_type == "orc":
        return {
            'name': 'Orc', 'health': 80, 'max_health': 80,
            'strength': 12, 'magic': 5, 'xp_reward': 50, 'gold_reward': 25
        }
    elif enemy_type == "dragon":
        return {
            'name': 'Dragon', 'health': 200, 'max_health': 200,
            'strength': 25, 'magic': 15, 'xp_reward': 200, 'gold_reward': 100
        }
    else:
        # This is for your Creativity Bonus if you add more
        # As long as the required 3 exist, this is fine.
        raise InvalidTargetError(f"Enemy type '{enemy_type}' not recognized.")

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        self.combat_active = False
        self.turn = 1
        self.ability_cooldown = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character['health'] <= 0:
            raise CharacterDeadError("Cannot start battle, character is dead.")
            
        self.combat_active = True
        self.turn = 1
        display_battle_log(f"A wild {self.enemy['name']} appears!")
        
        winner = None
        
        while self.combat_active:
            display_battle_log(f"--- Turn {self.turn} ---")
            
            self.player_turn()
            
            if not self.combat_active:
                winner = 'escaped'
                break
                
            winner = self.check_battle_end()
            if winner:
                break
                
            self.enemy_turn()
            
            winner = self.check_battle_end()
            if winner:
                break
                
            self.turn += 1
            if self.ability_cooldown > 0:
                self.ability_cooldown -= 1

        if winner == 'player':
            display_battle_log(f"You defeated the {self.enemy['name']}!")
            rewards = get_victory_rewards(self.enemy)
            
            character_manager.gain_experience(self.character, rewards['xp'])
            character_manager.add_gold(self.character, rewards['gold'])
            
            return {
                'winner': 'player', 
                'xp_gained': rewards['xp'], 
                'gold_gained': rewards['gold']
            }
        elif winner == 'enemy':
            display_battle_log("You have been defeated... Game Over.")
            return {'winner': 'enemy', 'xp_gained': 0, 'gold_gained': 0}
        else:
            display_battle_log("You fled from the battle.")
            return {'winner': 'none', 'xp_gained': 0, 'gold_gained': 0}
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise CombatNotActiveError("player_turn called when combat is not active.")
            
        display_combat_stats(self.character, self.enemy)
        
        print("\n--- Your Turn ---")
        print("1. Basic Attack")
        print(f"2. Special Ability ({self.character['class']})")
        print("3. Try to Run")
        
        choice = input("Choose your action (1-3): ")
        
        if choice == '1':
            display_battle_log("You attack!")
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"The {self.enemy['name']} takes {damage} damage.")
            
        elif choice == '2':
            if self.ability_cooldown > 0:
                display_battle_log(f"Ability on cooldown! {self.ability_cooldown} turns left.")
                return

            try:
                message = use_special_ability(self.character, self.enemy, self)
                display_battle_log(message)
                self.ability_cooldown = 3 
            except Exception as e:
                display_battle_log(f"Ability failed: {e}")
                
        elif choice == '3':
            self.attempt_escape()
            
        else:
            display_battle_log("Invalid choice. You hesitate and lose your turn.")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError("enemy_turn called when combat is not active.")

        display_battle_log(f"The {self.enemy['name']} attacks!")
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"You take {damage} damage.")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        if 'class' in attacker: # Attacker is player
            base_damage = attacker['strength']
        else:
            base_damage = attacker['strength']
        damage = base_damage - (defender['strength'] // 4)
        return max(1, damage)
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target['health'] -= damage
        target['health'] = max(0, target['health'])
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.character['health'] <= 0:
            self.combat_active = False
            return 'enemy'
        elif self.enemy['health'] <= 0:
            self.combat_active = False
            return 'player'
        
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        if random.random() < 0.5:
            display_battle_log("You successfully escaped!")
            self.combat_active = False # This will end the battle loop
            return True
        else:
            display_battle_log("You failed to escape!")
            return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    char_class = character['class']
    
    if char_class == 'Warrior':
        return warrior_power_strike(character, enemy, battle)
    elif char_class == 'Mage':
        return mage_fireball(character, enemy, battle)
    elif char_class == 'Rogue':
        return rogue_critical_strike(character, enemy, battle)
    elif char_class == 'Cleric':
        return cleric_heal(character, battle)
    else:
        return "You have no special ability."

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    damage = (character['strength'] * 2) - (enemy['strength'] // 4)
    damage = max(1, damage)
    battle.apply_damage(enemy, damage)
    return f"You use Power Strike for {damage} damage!"

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    damage = (character['magic'] * 2) - (enemy['magic'] // 4) # Simple magic defense
    damage = max(1, damage)
    battle.apply_damage(enemy, damage)
    return f"You cast Fireball for {damage} damage!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    if random.random() < 0.5: # 50% chance
        damage = (character['strength'] * 3) - (enemy['strength'] // 4)
        damage = max(1, damage)
        battle.apply_damage(enemy, damage)
        return f"CRITICAL STRIKE! You deal {damage} damage!"
    else:
        return "Your critical strike missed..."

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    healed_amount = character_manager.heal_character(character, 30)
    return f"You use Heal, restoring {healed_amount} HP."

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    pass

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

