import sys
import os
import random

# Add current directory to path so imports work if run from inside src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import DataLoader
from quiz_manager import VocabularyQuiz, GrammarQuiz

def clear_screen():
    # Simple clear for cleaner UI
    os.system('cls' if os.name == 'nt' else 'clear')

def select_file_from_list(files, file_type_name):
    if not files:
        print(f"No {file_type_name} files found.")
        return None
    
    print(f"\nSelect {file_type_name} file:")
    for i, f in enumerate(files):
        print(f"{i+1}. {os.path.basename(f)}")
    
    while True:
        choice = input("\nEnter file number: ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                return files[idx]
        print("Invalid selection. Try again.")

def run_vocabulary_quiz(loader):
    files = loader.get_vocabulary_files()
    target_file = select_file_from_list(files, "Vocabulary")
    if not target_file:
        return

    data = loader.load_vocabulary(target_file)
    if len(data) < 4:
        print("Not enough data to create variety options (need at least 4 words).")
        return

    print(f"\nLoaded {len(data)} words.")
    try:
        num = int(input(f"How many questions to test? (Max {len(data)}): "))
    except ValueError:
        num = len(data)
    
    quiz = VocabularyQuiz(data)
    quiz.prepare_quiz(num)
    
    score = 0
    total = len(quiz.questions)
    
    for i, q in enumerate(quiz.questions):
        print(f"\n[Question {i+1}/{total}]")
        print(f"Word: {q['text']}")
        
        for idx, opt in enumerate(q['options']):
            print(f"{idx+1}. {opt}")
            
        while True:
            ans = input("Your answer (1-4): ")
            if ans.isdigit() and 1 <= int(ans) <= 4:
                user_idx = int(ans) - 1
                if user_idx == q['correct_index']:
                    print("✅ Correct!")
                    score += 1
                else:
                    print(f"❌ Wrong! The correct meaning is: {q['options'][q['correct_index']]}")
                break
            else:
                print("Invalid input.")
                
    print(f"\n🎉 Quiz Finished! Score: {score}/{total}")
    input("Press Enter to return to menu...")

def run_grammar_quiz(loader):
    files = loader.get_grammar_files()
    target_file = select_file_from_list(files, "Grammar")
    if not target_file:
        return

    data = loader.load_grammar(target_file)
    if not data:
        print("No valid data found in file.")
        return

    print(f"\nLoaded {len(data)} grammar questions.")
    try:
        num = int(input(f"How many questions to test? (Max {len(data)}): "))
    except ValueError:
        num = len(data)
        
    quiz = GrammarQuiz(data)
    quiz.prepare_quiz(num)
    
    score = 0
    total = len(quiz.questions)
    
    for i, q in enumerate(quiz.questions):
        print(f"\n[Question {i+1}/{total}]")
        print(f"Fill in the blank: {q['text']}")
        # Hint is basically the question itself in this specific type, but let's show options
        
        for idx, opt in enumerate(q['options']):
            print(f"{idx+1}. {opt}")
            
        while True:
            ans = input("Your answer (1-2): ")
            if ans.isdigit() and 1 <= int(ans) <= 2:
                user_idx = int(ans) - 1
                if user_idx == q['correct_index']:
                    print("✅ Correct!")
                    score += 1
                else:
                    print(f"❌ Wrong! Correct: {q['options'][q['correct_index']]}")
                    if q.get('meaning'):
                        print(f"   (Meaning: {q['meaning']})")
                break
            else:
                print("Invalid input.")

    print(f"\n🎉 Quiz Finished! Score: {score}/{total}")
    input("Press Enter to return to menu...")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # If run from src, base_dir is parent. If run from root, we need to handle that.
    # Current assumption: file is at root/src/main.py. 
    # os.path.dirname(__file__) -> root/src
    # os.path.dirname(...) -> root
    # So base_dir is correct if structure is TEPS_Remember/src/main.py
    
    loader = DataLoader(base_dir)
    
    while True:
        clear_screen()
        print("=== TEPS Remember Quiz ===")
        print("1. Vocabulary Memorization (Test-1, Test-2...)")
        print("2. Grammar Memorization (To-v vs -ing)")
        print("3. Exit")
        
        choice = input("\nSelect mode: ")
        
        if choice == '1':
            run_vocabulary_quiz(loader)
        elif choice == '2':
            run_grammar_quiz(loader)
        elif choice == '3':
            print("Bye!")
            break
        else:
            input("Invalid selection. Press Enter...")

if __name__ == "__main__":
    main()
