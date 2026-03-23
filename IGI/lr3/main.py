"""
Purpose: Main user interface and execution loop
Lab: Laboratory Work 3
Version: 1.0
Developer: Kushniarou A D
Date: 2026-03-23
"""

import tasks
import initialization

def log_execution(func):
    """Decorator to log the start and end of function execution."""
    def wrapper(*args, **kwargs):
        print(f"\n[{func.__name__.upper()}] --- EXECUTION STARTED ---")
        result = func(*args, **kwargs)
        print(f"[{func.__name__.upper()}] --- EXECUTION FINISHED ---\n")
        return result
    return wrapper

@log_execution
def run_task1():
    try:
        x = float(input("Enter argument x for e^x: "))
        eps = float(input("Enter precision eps (e.g., 0.001): "))
        n, f_x, math_f_x = tasks.task1_series(x, eps)
        
        print("-" * 65)
        print(f"| {'x':^10} | {'n':^10} | {'F(x)':^15} | {'Math F(x)':^15} |")
        print("-" * 65)
        print(f"| {x:^10.4f} | {n:^10} | {f_x:^15.6f} | {math_f_x:^15.6f} |")
        print("-" * 65)
    except ValueError:
        print("Error: Invalid number format.")

@log_execution
def run_task2():
    print("Enter numbers to sum them up. Enter a number GREATER THAN 100 to stop.")
    total_sum = 0.0
    while True:
        try:
            val = float(input("> "))
            if val > 100:
                print("Number > 100 detected. Stopping loop.")
                break
            total_sum += val
        except ValueError:
            print("Error: Please enter a valid number.")
            
    print(f"Total sum of entered numbers: {total_sum}")

@log_execution
def run_task3():
    text = input("Enter a string for analysis: ")
    count = tasks.task3_count_lowercase_consonant_words(text)
    print(f"Number of words starting with a lowercase consonant: {count}")

@log_execution
def run_task4():
    target_string = ("«So she was considering in her own mind, as well as she could, "
                     "for the hot day made her feel very sleepy and stupid, whether "
                     "the pleasure of making a daisy-chain would be worth the trouble "
                     "of getting up and picking the daisies, when suddenly a White "
                     "Rabbit with pink eyes ran close by her.»")
                     
    print("Analyzing predefined string:\n", target_string)
    
    max_len_count, dot_comma_words, long_e_word = tasks.task4_analyze_alice(target_string)
    
    print(f"\na) Number of words with the maximum length: {max_len_count}")
    
    print("b) Words followed by a comma or a dot:")
    for w in dot_comma_words:
        print(f"   - {w}")
        
    print(f"c) The longest word ending in 'e': {long_e_word}")

@log_execution
def run_task5():
    try:
        size = int(input("Enter the size of the list: "))
        if size <= 0:
            print("Size must be a positive integer.")
            return
            
        choice = input("Initialize manually (m) or via random generator (r)? ").strip().lower()
        my_list = []
        
        if choice == 'm':
            initialization.init_via_input(my_list, size)
        elif choice == 'r':
            initialization.init_via_generator(my_list, size)
        else:
            print("Invalid initialization choice.")
            return
            
        print("\nGenerated list:", my_list)
        
        zeros, sum_after = tasks.task5_process_list(my_list)
        print(f"Amount of elements equal to 0: {zeros}")
        print(f"Sum of elements after the minimum absolute value element: {sum_after:.2f}")
        
    except ValueError:
        print("Error: Invalid integer input.")



def main():
    """Main application loop."""
    while True:
        print("\n" + "="*25)
        print("        MAIN MENU")
        print("="*25)
        print("1. Task 1 (e^x Taylor series)")
        print("2. Task 2 (Summing loop until > 100)")
        print("3. Task 3 (String analysis: lowercase consonant)")
        print("4. Task 4 (Alice text complex analysis)")
        print("5. Task 5 (Processing list of floats)")
        print("0. Exit program")
        
        choice = input("\nSelect a task: ").strip()
        
        if choice == '1': run_task1()
        elif choice == '2': run_task2()
        elif choice == '3': run_task3()
        elif choice == '4': run_task4()
        elif choice == '5': run_task5()
        elif choice == '0':
            print("Exiting... Have a good day!")
            break
        else:
            print("Invalid choice. Please select a number from 0 to 5.")

if __name__ == "__main__":
    main()
