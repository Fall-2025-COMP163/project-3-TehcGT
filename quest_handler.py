"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Tehcubelleh Keamu

AI Usage: Used google gemini for bug fix and missing function

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
import character_manager
# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")
        
    quest_info = quest_data_dict[quest_id]

    if is_quest_completed(character, quest_id):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' has already been completed.")

    if is_quest_active(character, quest_id):
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' is already active.")

    if character['level'] < quest_info['required_level']:
        raise InsufficientLevelError(
            f"Cannot accept '{quest_id}'. "
            f"Requires level {quest_info['required_level']}, "
            f"you are level {character['level']}."
        )

    prereq = quest_info['prerequisite']
    if prereq != "NONE" and not is_quest_completed(character, prereq):
        raise QuestRequirementsNotMetError(
            f"Cannot accept '{quest_id}'. "
            f"Prerequisite quest '{prereq}' is not completed."
        )
    character['active_quests'].append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")
        
    quest_info = quest_data_dict[quest_id]

    if not is_quest_active(character, quest_id):
        raise QuestNotActiveError(f"Cannot complete '{quest_id}': it is not an active quest.")

    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)

    xp_reward = quest_info['reward_xp']
    gold_reward = quest_info['reward_gold']
    
    try:
        character_manager.gain_experience(character, xp_reward)
    except character_manager.CharacterDeadError:
        print("Gained XP, but cannot level up while dead.")
        
    character_manager.add_gold(character, gold_reward)

    rewards = {'xp': xp_reward, 'gold': gold_reward}
    return rewards

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    if not is_quest_active(character, quest_id):
        raise QuestNotActiveError(f"Cannot abandon '{quest_id}': it is not an active quest.")
        
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    return [
        quest_data_dict[qid] for qid in character['active_quests'] 
        if qid in quest_data_dict
    ]

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    return [
        quest_data_dict[qid] for qid in character['completed_quests'] 
        if qid in quest_data_dict
    ]

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    return [
        quest_data for quest_id, quest_data in quest_data_dict.items() 
        if can_accept_quest(character, quest_id, quest_data_dict)
    ]

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character['completed_quests']

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character['active_quests']

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    try:
        quest_info = quest_data_dict[quest_id]
        
        if character['level'] < quest_info['required_level']:
            return False
            
        prereq = quest_info['prerequisite']
        if prereq != "NONE" and not is_quest_completed(character, prereq):
            return False
            
        if is_quest_completed(character, quest_id):
            return False
            
        if is_quest_active(character, quest_id):
            return False
            
    except KeyError:
        return False
        
    return True
def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    chain = []
    current_id = quest_id

    while current_id and current_id != "NONE":
        if current_id not in quest_data_dict:
            raise QuestNotFoundError(
                f"Prerequisite '{current_id}' in chain for '{quest_id}' not found."
            )

        chain.append(current_id)
        current_id = quest_data_dict[current_id].get("prerequisite")

        # Detect cycles: A → B → A
        if current_id in chain:
            raise QuestRequirementsNotMetError(
                f"Quest prerequisite cycle detected for '{quest_id}'."
            )

    return chain[::-1]

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
        
    completed_quests = len(character['completed_quests'])
    return (completed_quests / total_quests) * 100.0

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    total_xp = 0
    total_gold = 0
    
    for quest_id in character['completed_quests']:
        if quest_id in quest_data_dict:
            quest_info = quest_data_dict[quest_id]
            total_xp += quest_info['reward_xp']
            total_gold += quest_info['reward_gold']
            
    return {'total_xp': total_xp, 'total_gold': total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    return [
        quest_data for quest_data in quest_data_dict.values()
        if min_level <= quest_data['required_level'] <= max_level
    ]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display 
    print(f"\n=== {quest_data['title']} ===")
    print(f"  Level: {quest_data['required_level']}  |  Prereq: {quest_data['prerequisite']}")
    print(f"  Description: {quest_data['description']}")
    print(f"  Rewards: {quest_data['reward_xp']} XP, {quest_data['reward_gold']} Gold")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    list_title = "Quests"
    
    print(f"\n--- {list_title} ---")
    
    if not quest_list:
        print("  (No quests to display)")
        return
        
    for quest_data in quest_list:
        print(f"- {quest_data['title']} (Lvl {quest_data['required_level']}) | "
              f"Rewards: {quest_data['reward_xp']} XP, {quest_data['reward_gold']} Gold")

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    print("\n--- QUEST PROGRESS ---")
    print(f"  Active Quests: {len(character['active_quests'])}")
    print(f"  Completed Quests: {len(character['completed_quests'])}")
    
    percentage = get_quest_completion_percentage(character, quest_data_dict)
    print(f"  Completion: {percentage:.2f}%")
    
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    print(f"  Total XP Earned: {rewards['total_xp']}")
    print(f"  Total Gold Earned: {rewards['total_gold']}")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for quest_id, quest_data in quest_data_dict.items():
        prereq = quest_data.get('prerequisite')
        if prereq != "NONE" and prereq not in quest_data_dict:
            print(f"WARNING: Quest '{quest_id}' requires missing quest '{prereq}'")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

