import random
import string

# Function to generate a random password based on user preferences.
def generate_password(length, use_digits, use_uppercase, use_lowercase, use_symbols):
    """
    Generates a password with at least one character from each chosen category.
    Steps:
    - Create a list of selected character groups.
    - Pick one random character from each group to ensure diversity.
    - Fill in the rest of the password length with a random mix.
    - Shuffle for extra randomness.
    """
    char_types = []  # Store selected character sets in a list

    # Append chosen character types
    if use_digits:
        char_types.append(string.digits)  # '0123456789'
    if use_uppercase:
        char_types.append(string.ascii_uppercase)  # 'A-Z'
    if use_lowercase:
        char_types.append(string.ascii_lowercase)  # 'a-z'
    if use_symbols:
        char_types.append(string.punctuation)  # Special characters like @#$%^&*

    # Safety check: Prevent empty set
    if not char_types:
        raise ValueError("At least one character type must be selected")

    # STEP 1: Start by picking one character from each selected group.
    password = [random.choice(chars) for chars in char_types]

    # STEP 2: Fill in remaining characters randomly from all available types.
    remaining_length = length - len(password)
    all_chars = ''.join(char_types)
    password += [random.choice(all_chars) for _ in range(remaining_length)]

    # STEP 3: Shuffle so that first few chars aren't predictable.
    random.shuffle(password)

    # Convert list to string
    return ''.join(password)

# Function to interactively gather user preferences.
def get_user_preferences():
    """
    Asks the user for password length and character type preferences.
    Returns a tuple containing all choices.
    """
    # Helper function to handle Yes/No input
    def ask(prompt):
        return input(prompt).strip().lower() in ['yes', 'y']

    # Ask for password length and preferences
    length = int(input("Enter the desired password length: "))
    use_digits = ask("Include digits? (yes/no): ")
    use_uppercase = ask("Include uppercase letters? (yes/no): ")
    use_lowercase = ask("Include lowercase letters? (yes/no): ")
    use_symbols = ask("Include symbols? (yes/no): ")
    return length, use_digits, use_uppercase, use_lowercase, use_symbols

# Function to generate a memory hint for the user.
def generate_hint(password, use_digits, use_uppercase, use_lowercase, use_symbols):
    """
    Creates a hint that helps the user recall their password
    without revealing the entire thing.
    """
    hint_parts = []
    if use_digits:
        hint_parts.append("has digits")
    if use_uppercase:
        hint_parts.append("has uppercase letters")
    if use_lowercase:
        hint_parts.append("has lowercase letters")
    if use_symbols:
        hint_parts.append("has symbols")

    # Use the first 3 chars as a safe 'seed' memory clue
    seed = password[:3]
    types_hint = ', '.join(hint_parts)
    hint = f"Your password starts with '{seed}' and {types_hint}."
    return hint

# Main function to put everything together
def main():
    """
    Orchestrates:
    - Gathering preferences
    - Generating password
    - Providing an easy hint for memory
    """
    # Step 1: Get preferences from user
    length, use_digits, use_uppercase, use_lowercase, use_symbols = get_user_preferences()

    # Step 2: Generate secure password based on preferences
    password = generate_password(length, use_digits, use_uppercase, use_lowercase, use_symbols)

    # Step 3: Create a memory-friendly hint
    hint = generate_hint(password, use_digits, use_uppercase, use_lowercase, use_symbols)

    # Step 4: Display results
    print(f"Your generated password is: {password}")
    print(f"Memory Hint: {hint}")

# Ensures this script runs only when executed directly
if __name__ == "__main__":
    main()
