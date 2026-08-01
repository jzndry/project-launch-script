#!/usr/bin/env python3
"""
Interactive Project Launcher Generator
Creates executable zsh scripts that loads a file in one of two code editors in ~/Projects/scripts
"""

import os
import stat
import sys
from pathlib import Path

# Define the directory for generated scripts
TARGET_DIR = Path.home() / "Projects" / "scripts"

# Zsh shell template with clean echo formatting
SHELL_TEMPLATE = """#!/usr/bin/env zsh
# Generated project launcher for {project_name}

echo "Launching {project_name}..."

# 1. Navigate to project directory
cd "{project_path}" || exit 1


# 3. Open VS Code for the project directory
echo "💻 Opening VS Code..."
code .

echo "✅ {project_name} is ready!"
"""


def get_input(prompt_text, default_value=None, required=False):
    """
    Helper function to handle user prompts, defaults, and validation.
    
    arguments:
    prompt_text: str - The text to display to the user.
    default_value: str or None - The default value to use if the user provides no input
    required: bool - If True, the user must provide a value (or a default must be set).

    returns:
    str - The user's input, or the default value if provided and no input was given.
        If the field is not required and no input is given, returns an empty string.
        If the field is required and no input is given, it will keep prompting until a valid input is received. 
    """

    if default_value:
        display_prompt = f"{prompt_text} [{default_value}]: "
    else:
        display_prompt = f"{prompt_text}: "

    while True:
        user_val = input(display_prompt).strip()
        
        # Fall back to default if input is empty and we have a default
        if not user_val and default_value:
            return default_value
        
        # If required and no default, keep asking
        if not user_val and required:
            print("This field cannot be empty. Please enter a value.")
            continue
            
        if user_val:
            return user_val
            
        return "" # If not required and no input, return empty string


def main():
    
    print("\n--------------------------------------------------")
    print("     Interactive Project Launcher Generator")
    print("--------------------------------------------------\n")
    print("To quit at any time, press Ctrl+C.\n")

    if not TARGET_DIR.exists():
        print("Error: Target directory does not exist. Please update interactive-prompt.py first.")
        sys.exit(1)

    name = get_input("1. Project name", required=True)
    
    raw_path = get_input("2. Path to project directory", default_value = Path.home() / "Projects" / name)
    # Expand ~ user symbols and resolve absolute path
    resolved_path = Path(raw_path).expanduser().resolve()

    if not resolved_path.exists():
        print(f"Error: The provided path '{resolved_path}' does not exist. Please check and try again.")
        sys.exit(1)

    # Populate the script template
    script_content = SHELL_TEMPLATE.format(
        project_name=name,
        project_path=resolved_path,
        git_branch="main"
    )

    # Sanitise filename: lowecase with underscores (e.g., load_my_project)
    clean_filename = f"load_{name.lower().replace(' ', '_')}"
    target_file = TARGET_DIR / clean_filename

    with open(target_file, "w") as f:
        f.write(script_content)

    # 5. Make executable (chmod +x equivalent in Python)
    current_permissions = os.stat(target_file).st_mode
    os.chmod(target_file, current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print("\n--------------------------------------------------")
    print(f"🎉 Success! Launcher created at:")
    print(f"   {target_file}")
    print(f"\nYou can now run this command from anywhere:")
    print(f"   {clean_filename}")
    print("--------------------------------------------------\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user. Exiting cleanly.")
        sys.exit(0)