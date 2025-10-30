import os # Used for checking if a file exists in load_character

# --- PROJECT METADATA ---
"""
COMP 163 - Project 1: Character Creator & Saving/Loading
Name: [Talib Lyon]
Date: [10/22/25]

AI Usage: Barely any AI was used. Minor assistance was requested to integrate the required function signatures and confirm error handling methods for file I/O, adhering to the "no classes" constraint.
"""

# --- CONFIGURATION ---

# The character's level 1 GOLD is a starting constant (Bonus Creative Element: Simple Gold System).
STARTING_GOLD = 100 

# Stat Definition: (STR_base, MAG_base, HP_base, STR_growth, MAG_growth, HP_growth)
# Design Choice: Fantasy-themed stats with distinct class roles
# Stat Formula is: Stat = Base + (Level * Growth)
CLASS_STATS = {
    "WARRIOR": (12, 4, 100, 4, 1, 30), # High strength, low magic, high health
    "MAGE":    (4, 15, 80, 1, 5, 20),  # Low strength, high magic, medium health
    "ROGUE":   (8, 8, 90, 2, 2, 25),  # Medium strength, medium magic, medium health
    "CLERIC":  (8, 10, 110, 2, 3, 35), # Medium strength, high magic, very high health
}

# --- REQUIRED FUNCTIONS ---

def calculate_stats(character_class, level):
    """
    Calculates base stats based on class and level.
    
    STAT FORMULA (My Design Choice): Stat = Base + (Level * Growth)
    
    Returns: tuple of (strength, magic, health)
    """
    validated_class = character_class.upper()
    
    if validated_class not in CLASS_STATS:
        # Should not be reached if create_character validates input, but provides a fallback
        return 0, 0, 0 

    # Unpack the configuration data in the defined order
    str_base, mag_base, hp_base, str_growth, mag_growth, hp_growth = CLASS_STATS[validated_class]
    
    # Calculate stats using the linear formula
    strength = str_base + (level * str_growth)
    magic = mag_base + (level * mag_growth)
    health = hp_base + (level * hp_growth)
    
    # Return a tuple as requested
    return strength, magic, health


def create_character(name, character_class):
    """
    Creates a new character dictionary with calculated stats.
    
    Returns: character dictionary if successful, None if class is invalid.
    
    Example:
    char = create_character("Aria", "Mage")
    # Should return: {"name": "Aria", "class": "Mage", "level": 1, "strength": 5, "magic": 15, "health": 80, "gold": 100}
    """
    validated_class = character_class.upper()
    
    # Required Error Handling: Validate character class input
    if validated_class not in CLASS_STATS:
        print(f"ERROR: Invalid class '{character_class}'. Valid classes are: {', '.join(CLASS_STATS.keys())}")
        return None

    # Calculate initial stats (Level 1)
    strength, magic, health = calculate_stats(validated_class, 1)

    # Build the character dictionary
    character = {
        "Name": name,
        "Class": validated_class,
        "Level": 1,
        "Strength": strength,
        "Magic": magic,
        "Health": health,
        "Gold": STARTING_GOLD
    }
    
    print(f"\nSUCCESS: Character '{name}' ({validated_class}) created at Level 1.")
    return character


def level_up(character):
    """
    Increases character level and recalculates stats.
    Modifies the character dictionary directly.
    Returns: None
    """
    if not character:
        print("Cannot level up: Character is missing.")
        return

    # 1. Increase the level
    character["Level"] += 1
    
    # 2. Recalculate stats based on the new level
    strength, magic, health = calculate_stats(character["Class"], character["Level"])
    
    # 3. Update stats in the character dictionary
    character["Strength"] = strength
    character["Magic"] = magic
    character["Health"] = health
    
    print(f"LEVEL UP! {character['Name']} is now Level {character['Level']}!")
    # Note: Gold remains constant on level up in this model.


def save_character(character, filename):
    """
    Saves character to text file in specific format.
    Returns: True if successful, False if error occurred.
    """
    # Required file format using descriptive keys (must match load_character)
    content = (
        f"Character Name: {character['Name']}\n"
        f"Class: {character['Class']}\n"
        f"Level: {character['Level']}\n"
        f"Strength: {character['Strength']}\n"
        f"Magic: {character['Magic']}\n"
        f"Health: {character['Health']}\n"
        f"Gold: {character['Gold']}\n"
    )

    try:
        # Required Error Handling: Handle permission errors
        with open(filename, 'w') as f:
            f.write(content)
        print(f"SUCCESS: Character '{character['Name']}' saved to {filename}")
        return True
    except IOError as e:
        # IOError catches PermissionError, disk errors, etc.
        print(f"ERROR: Could not save character to {filename}. I/O Error: {e}")
        return False


def load_character(filename):
    """
    Loads character from text file.
    Returns: character dictionary if successful, None if file not found or corrupted.
    """
    # Required Error Handling: Handle file not found errors
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found.")
        return None

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except IOError as e:
        # Handle read-permission or other read-related I/O errors
        print(f"ERROR: Could not read file {filename}. I/O Issue: {e}")
        return None
        
    character = {}
    
    # Mapping the file's descriptive key to the character dictionary's simple key
    MAPPING = {
        "Character Name": "Name",
        "Class": "Class",
        "Level": "Level",
        "Strength": "Strength",
        "Magic": "Magic",
        "Health": "Health",
        "Gold": "Gold"
    }
    
    # Process each line
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            # Split into Key: Value
            key_full, value_str = line.split(':', 1)
            key_full = key_full.strip()
            value_str = value_str.strip()
            
            if key_full in MAPPING:
                target_key = MAPPING[key_full]
                
                # Convert appropriate values to integers
                if target_key in ["Level", "Strength", "Magic", "Health", "Gold"]:
                    character[target_key] = int(value_str)
                else: # Name and Class are strings
                    character[target_key] = value_str
            
        except ValueError:
            # Catches issues like a non-numeric value in a numeric field
            print(f"WARNING: Skipping corrupted value for {key_full} in line: {line}")
        except:
             # Catches issues like line missing the colon separator
             print(f"WARNING: Skipping improperly formatted line: {line}")

    # Final check for data integrity
    required_keys = ["Name", "Class", "Level", "Strength", "Magic", "Health", "Gold"]
    if not all(k in character for k in required_keys):
         print(f"ERROR: File {filename} is missing essential character data.")
         return None
    
    # Optional: Basic class validation on loaded data
    if character.get('Class', '').upper() not in CLASS_STATS:
        print(f"ERROR: Loaded character has invalid class: {character.get('Class')}")
        return None
        
    print(f"SUCCESS: Character '{character['Name']}' loaded from {filename}")
    return character


def display_character(character):
    """
    Prints formatted character sheet.
    Returns: None (prints to console).
    """
    if not character:
        print("No character data to display.")
        return

    print("\n=== CHARACTER SHEET ===")
    print(f"Name:     {character.get('Name', 'N/A')}")
    print(f"Class:    {character.get('Class', 'N/A')}")
    print(f"Level:    {character.get('Level', 0)}")
    print("-------------------------")
    print(f"Strength: {character.get('Strength', 0)}")
    print(f"Magic:    {character.get('Magic', 0)}")
    print(f"Health:   {character.get('Health', 0)}")
    print(f"Gold:     {character.get('Gold', 0)}")
    print("=========================\n")


# Main program area (optional - for testing your functions)
if __name__ == "__main__":
    print("=== CHARACTER CREATOR DEMO ===")
    
    # --- 1. Test Creation and Display (Mage example) ---
    print("\n--- 1. Testing Creation (Mage) ---")
    # Example: char = create_character("Aria", "Mage")
    aria = create_character("Aria", "Mage")
    if aria:
        display_character(aria)
        
        # --- 2. Test Level Up ---
        print("\n--- 2. Testing Level Up ---")
        level_up(aria) # Level 2
        level_up(aria) # Level 3
        display_character(aria)
        
        # --- 3. Test Saving ---
        print("\n--- 3. Testing Saving (aria_chronicles.txt) ---")
        save_character(aria, "aria_chronicles.txt")
        
        # --- 4. Test Loading ---
        print("\n--- 4. Testing Loading ---")
        loaded_aria = load_character("aria_chronicles.txt")
        display_character(loaded_aria)
        
        # --- 5. Test Invalid Class Error Handling (Required) ---
        print("\n--- 5. Testing Invalid Class Error ---")
        invalid_char = create_character("BadHero", "Archivist")
        if invalid_char is None:
            print("Test Passed: Invalid class creation successfully blocked.")

        # --- 6. Test File Not Found Error Handling (Required) ---
        print("\n--- 6. Testing File Not Found Error ---")
        missing_char = load_character("non_existent_file.txt")
        if missing_char is None:
            print("Test Passed: File Not Found error successfully handled.")

        # --- 7. Test Warrior Example (Level 5) ---
        print("\n--- 7. Testing Warrior Creation and Level 5 Stats ---")
        grog = create_character("Grog", "Warrior")
        if grog:
             for _ in range(4): # Level up 4 times to reach Level 5
                level_up(grog)
             display_character(grog)
             save_character(grog, "grog_chronicles.txt")
