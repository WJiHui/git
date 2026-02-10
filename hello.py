#!/usr/bin/env python3
"""
Hello World Script
A simple Python script that prints hello messages.
"""

import sys
import argparse
from datetime import datetime


def print_simple_hello():
    """Print a simple hello message."""
    print("Hello, World!")


def print_personalized_hello(name="World"):
    """Print a personalized hello message."""
    print(f"Hello, {name}!")


def print_multilingual_hello():
    """Print hello in multiple languages."""
    greetings = {
        "English": "Hello",
        "Spanish": "Hola",
        "French": "Bonjour",
        "German": "Hallo",
        "Chinese": "你好",
        "Japanese": "こんにちは",
        "Korean": "안녕하세요",
        "Russian": "Привет",
        "Arabic": "مرحبا",
        "Hindi": "नमस्ते"
    }
    
    print("Greetings in different languages:")
    for language, greeting in greetings.items():
        print(f"  {language}: {greeting}")


def print_timed_hello():
    """Print a hello message with current time."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Hello! Current time is: {current_time}")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="A hello world script with various options"
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        default="World",
        help="Specify a name to greet (default: World)"
    )
    parser.add_argument(
        "-m", "--multilingual",
        action="store_true",
        help="Show hello in multiple languages"
    )
    parser.add_argument(
        "-t", "--time",
        action="store_true",
        help="Show hello with current time"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show all hello variations"
    )
    
    args = parser.parse_args()
    
    print("=" * 40)
    print("Hello Script")
    print("=" * 40)
    
    if args.all:
        # Show all variations
        print_simple_hello()
        print()
        print_personalized_hello(args.name)
        print()
        print_multilingual_hello()
        print()
        print_timed_hello()
    else:
        # Show selected variations
        if not any([args.multilingual, args.time]):
            # Default: show simple and personalized
            print_simple_hello()
            print_personalized_hello(args.name)
        
        if args.multilingual:
            print_multilingual_hello()
        
        if args.time:
            print_timed_hello()
    
    print("=" * 40)
    print("Script completed successfully!")


if __name__ == "__main__":
    main()