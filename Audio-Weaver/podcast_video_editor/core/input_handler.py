import os
from ..utils.time_parser import parse_time_string

class InputHandler:
    def get_file_path(self, prompt_text, extensions=None):
        while True:
            path = input(prompt_text).strip()
            # Remove quotes if user dragged and dropped file
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]
            if path.startswith("'") and path.endswith("'"):
                path = path[1:-1]
                
            if os.path.exists(path):
                if extensions:
                    if not any(path.lower().endswith(ext) for ext in extensions):
                        print(f"Invalid file type. Expected: {', '.join(extensions)}")
                        continue
                return path
            print(f"Error: File not found at {path}. Please try again.")

    def get_int(self, prompt_text, min_val=None):
        while True:
            try:
                val = int(input(prompt_text))
                if min_val is not None and val < min_val:
                    print(f"Value must be at least {min_val}.")
                    continue
                return val
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_time(self, prompt_text):
        while True:
            try:
                return parse_time_string(input(prompt_text))
            except ValueError:
                print("Invalid time format. Use HH:MM:SS.")
    
    def get_choice(self, prompt_text, choices):
        while True:
            val = input(prompt_text).lower().strip()
            if val in choices:
                return val
            print(f"Invalid choice. Options: {', '.join(choices)}")
    
    def get_yes_no(self, prompt_text):
        while True:
            val = input(prompt_text + " (y/n): ").lower().strip()
            if val in ['y', 'yes']:
                return True
            if val in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'.")
