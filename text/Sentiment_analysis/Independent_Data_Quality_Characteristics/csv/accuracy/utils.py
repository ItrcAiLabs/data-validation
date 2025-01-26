import re
import string
import nltk
from nltk.corpus import stopwords
from hazm import Normalizer, word_tokenize, stopwords_list

# Define a string of Persian punctuations to be removed
# This includes common punctuation symbols used in Persian text
persian_punctuations = '''`÷×؛#<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''

# Combine the standard English punctuation with Persian punctuation
# This allows us to handle both types of punctuations in a single list
punctuations_list = string.punctuation + persian_punctuations

# Define a regular expression to capture Arabic diacritics
# These are marks that modify the pronunciation of letters in Arabic and Persian (i.e., Fatha, Damma, Kasra, etc.)
arabic_diacritics = re.compile("""
                          ّ    | # Tashdid (doubling of consonants)
                          َ    | # Fatha (a short vowel mark above a letter)
                          ً    | # Tanwin Fath (a form of the Fatha)
                          ُ    | # Damma (a short vowel mark above a letter)
                          ٌ    | # Tanwin Damm (a form of the Damma)
                          ِ    | # Kasra (a short vowel mark below a letter)
                          ٍ    | # Tanwin Kasr (a form of the Kasra)
                          ْ    | # Sukun (indicates absence of a vowel)
                          ـ     # Tatwil/Kashida (a stretch symbol used in Arabic script)
                      """, re.VERBOSE)  # Verbose allows multi-line regular expressions for readability

def remove_persian_punctuation(text : str) -> str:
    """
    Function to remove Persian and English punctuation marks from a text.

    Args:
    text (str): Input string containing Persian/English punctuation marks.

    Returns:
    str: The text with all punctuation marks removed.
    """
    # Create a translation table to replace all specified characters (punctuation) with None
    # str.maketrans creates a map for character replacements
    translator = str.maketrans('', '', punctuations_list)
    
    # Using translate() to remove all punctuations from the text
    return text.translate(translator)

def remove_arabic_diacritics(text : str) -> str:
    """
    Function to remove Arabic diacritical marks from the text.
    
    Args:
    text (str): Input string containing Arabic diacritics.
    
    Returns:
    str: The text with Arabic diacritics removed.
    """
    # Use regex substitution to replace all occurrences of Arabic diacritic marks
    # with an empty string (i.e., removing them)
    text = re.sub(arabic_diacritics, '', text)
    
    # Return the cleaned text without diacritics
    return text

def remove_informal_words(text: str) -> str:
    """
    Function to remove informal and colloquial words from the text based on a predefined list.

    Args:
    text (str): Input string containing informal words.

    Returns:
    str: The cleaned text with informal words removed.
    """
    # List of informal words or colloquial phrases commonly used in Persian language
    informal_words = [
        r"\bمیخوام\b", r"\bنمیخوام\b", r"\bمیریم\b", r"\bبخوام\b", r"\bمیگم\b", r"\bمیگه\b", 
        r"\bمیگن\b", r"\bبریم\b", r"\bبرمیگردیم\b", r"\bنمیدونم\b", r"\bنمیتونم\b", r"\bنمیشه\b", 
        r"\bبزار\b", r"\bبده\b", r"\bمیدم\b", r"\bمیدن\b", r"\bدارم\b", r"\bندارم\b", r"\bچطوری\b", 
        r"\bمیبینم\b", r"\bاینو\b", r"\bاونجا\b", r"\bاینکه\b", r"\bاون\b", r"\bدلم میخواد\b", 
        r"\bچیکار کنم\b", r"\bکی\b", r"\bکجا\b", r"\bحالا\b", r"\bالان\b", r"\bآره\b", r"\bنه\b", 
        r"\bباشه\b", r"\bمیخواستم\b", r"\bبخواستم\b", r"\bخوبه\b", r"\bهمینه\b", r"\bچرا\b", 
        r"\bمیشه\b", r"\bمیکنم\b", r"\bکردن\b", r"\bمیکنه\b", r"\bدست میارم\b", r"\bبرگردیم\b", 
        r"\bمنم\b", r"\bتوئه\b", r"\bخودم\b", r"\bخودش\b", r"\bخودمون\b", r"\bخودتون\b", 
        r"\bخودشون\b", r"\bاگه\b"  # Colloquial phrases
    ]
    
    # Loop through each informal word/phrase and remove it using regex substitution
    # The \b ensures that only whole words are removed (not partial matches)
    for word in informal_words:
        text = re.sub(word, '', text)
    
    # After all informal words are removed, return the cleaned text
    return text.strip()  # Strip any leading or trailing spaces

def remove_stopwords(text : str) -> str:
    """
    Function to remove stopwords from the text using Hazm's stopword list.

    Args:
    text (str): Input string containing words to filter.

    Returns:
    str: The cleaned text without stopwords.
    """
    # Tokenize the text into individual words
    words = word_tokenize(text)  # Hazm tokenizer for Persian text
    
    # Get Hazm's list of Persian stopwords
    stop_words = set(stopwords_list())  # Fetch the stopwords from Hazm library
    
    # Filter out words that are in the stopwords list
    filtered_words = [word for word in words if word not in stop_words]
    
    # Return the filtered text by joining the words back together
    return ' '.join(filtered_words)
