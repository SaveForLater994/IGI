"""
Purpose: Business logic for Variant 15 tasks
Lab: Laboratory Work 3
Version: 1.0
Developer: Kushniarou A D
Date: 2026-03-23
"""

import math
import string

def task1_series(x: float, eps: float) -> tuple:
    """
    Calculates e^x using Maclaurin series up to a given precision eps.
    """
    n = 0
    term = 1.0
    series_sum = 0.0
    
    while abs(term) >= eps and n < 500:
        series_sum += term
        n += 1
        term *= x / n  # Next term in the series (x^n / n!)
        
    math_val = math.exp(x)
    return n, series_sum, math_val

def task3_count_lowercase_consonant_words(text: str) -> int:
    """
    Counts words starting with a lowercase consonant.
    """
    consonants = "bcdfghjklmnpqrstvwxyzбвгджзйклмнпрстфхцчшщ"
    count = 0
    words = text.split()
    
    for word in words:
        # Strip punctuation from the start to get the actual first letter
        clean_word = word.strip(string.punctuation)
        if clean_word and clean_word.islower() and clean_word in consonants:
            count += 1
            
    return count

def task4_analyze_alice(text: str) -> tuple:
    """
    Analyzes the predefined Alice in Wonderland string.
    a) Amount of words with maximum length
    b) Words followed by a comma or a dot
    c) The longest word ending in 'e'
    """
    words_raw = text.split()
    
    # Clean words for length calculation
    clean_words = [w.strip(string.punctuation + '«»') for w in words_raw]
    clean_words = [w for w in clean_words if w] # Remove empty strings
    
    # a) Words with max length
    if not clean_words:
        return 0, [], ""
        
    max_len = max(len(w) for w in clean_words)
    max_len_count = sum(1 for w in clean_words if len(w) == max_len)
    
    # b) Words followed by a comma or dot
    # We check the original raw words to see if they end with ',' or '.'
    words_with_comma_or_dot = []
    for w in words_raw:
        if w.endswith(',') or w.endswith('.') or w.endswith(',»') or w.endswith('.»'):
            words_with_comma_or_dot.append(w.strip(string.punctuation + '«»'))
            
    # c) Longest word ending in 'e'
    words_ending_in_e = [w for w in clean_words if w.lower().endswith('e')]
    longest_e_word = max(words_ending_in_e, key=len) if words_ending_in_e else ""
    
    return max_len_count, words_with_comma_or_dot, longest_e_word

def task5_process_list(lst: list) -> tuple:
    """
    Processes a list of floats.
    Returns the count of zero elements and the sum of elements
    located after the minimum by absolute value element.
    """
    if not lst:
        return 0, 0.0
        
    zero_count = lst.count(0.0)
    
    # Find the index of the element with the minimum absolute value
    min_mod_val = min(lst, key=abs)
    min_mod_idx = lst.index(min_mod_val)
    
    # Sum of elements after the minimum absolute value element
    sum_after = sum(lst[min_mod_idx + 1:]) if min_mod_idx + 1 < len(lst) else 0.0
        
    return zero_count, sum_after
