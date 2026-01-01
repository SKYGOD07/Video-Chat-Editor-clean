"""User input handling and validation."""

import os
from pathlib import Path


class InputHandler:
    """Handles all user input and file validation."""
    
    @staticmethod
    def get_file_path(prompt: str, file_type: str = "video") -> str:
        """
        Prompt user for a file path and validate it exists.
        
        Args:
            prompt: Display prompt
            file_type: Type of file being requested
            
        Returns:
            Validated file path
        """
        while True:
            file_path = input(f"\n{prompt}: ").strip()
            
            if not file_path:
                print(f"❌ {file_type.capitalize()} path cannot be empty")
                continue
            
            # Handle quotes
            file_path = file_path.strip('"\'')
            
            # Convert to absolute path
            file_path = str(Path(file_path).resolve())
            
            # Validate file exists
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                continue
            
            # Validate it's a file
            if not os.path.isfile(file_path):
                print(f"❌ Path is not a file: {file_path}")
                continue
            
            print(f"✓ {file_type.capitalize()} loaded: {file_path}")
            return file_path
    
    @staticmethod
    def get_integer(prompt: str, min_val: int = 1, max_val: int = None) -> int:
        """
        Prompt user for integer input with validation.
        
        Args:
            prompt: Display prompt
            min_val: Minimum allowed value
            max_val: Maximum allowed value (optional)
            
        Returns:
            Validated integer
        """
        while True:
            try:
                value = int(input(f"\n{prompt}: ").strip())
                
                if value < min_val:
                    print(f"❌ Value must be at least {min_val}")
                    continue
                
                if max_val is not None and value > max_val:
                    print(f"❌ Value must be at most {max_val}")
                    continue
                
                return value
            except ValueError:
                print("❌ Please enter a valid integer")
    
    @staticmethod
    def get_choice(prompt: str, options: list[str]) -> str:
        """
        Prompt user to choose from options.
        
        Args:
            prompt: Display prompt
            options: List of valid options
            
        Returns:
            Selected option
        """
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = int(input("\nEnter number: ").strip())
                
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                
                print(f"❌ Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    @staticmethod
    def get_yes_no(prompt: str) -> bool:
        """
        Prompt user for yes/no input.
        
        Args:
            prompt: Display prompt
            
        Returns:
            True for yes, False for no
        """
        while True:
            response = input(f"\n{prompt} (y/n): ").strip().lower()
            
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no'):
                return False
            else:
                print("❌ Please enter 'y' or 'n'")
    
    @staticmethod
    def print_header(title: str):
        """Print formatted section header."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    @staticmethod
    def print_success(message: str):
        """Print success message."""
        print(f"\n✓ {message}")
    
    @staticmethod
    def print_error(message: str):
        """Print error message."""
        print(f"\n❌ {message}")
    
    @staticmethod
    def print_info(message: str):
        """Print info message."""
        print(f"\nℹ {message}")
