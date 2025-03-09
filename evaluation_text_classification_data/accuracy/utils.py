import re
import string
import emoji
from hazm import Normalizer, word_tokenize, stopwords_list
#import dadmatools.pipeline.language as language




class CleanText:
    def __init__(self) -> None:


        # Initialize DadmaTools spellchecker pipeline
        #self.spell_checker =  language.Pipeline('spellchecker')


        # Define a string of Persian punctuations to be removed
        # This includes common punctuation symbols used in Persian text
        self.persian_punctuations = '''`÷×؛#<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''

        # Combine the standard English punctuation with Persian punctuation
        # This allows us to handle both types of punctuations in a single list
        self.punctuations_list = string.punctuation + self.persian_punctuations

        # Define a regular expression to capture Arabic diacritics
        # These are marks that modify the pronunciation of letters in Arabic and Persian (i.e., Fatha, Damma, Kasra, etc.)
        self.arabic_diacritics = re.compile("""
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
                
        # List of informal words or colloquial phrases commonly used in Persian language
        self.informal_words = [
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
    
        # Get Hazm's list of Persian stopwords
        self.stop_words = set(stopwords_list())  # Fetch the stopwords from Hazm library


    def remove_persian_punctuation(self, text : str) -> str:
        """
        Function to remove Persian and English punctuation marks from a text.

        Args:
        text (str): Input string containing Persian/English punctuation marks.

        Returns:
        str: The text with all punctuation marks removed.
        """
        # Create a translation table to replace all specified characters (punctuation) with None
        # str.maketrans creates a map for character replacements
        translator = str.maketrans('', '', self.punctuations_list)
        
        # Using translate() to remove all punctuations from the text
        return text.translate(translator)

    def remove_arabic_diacritics(self, text : str) -> str:
        """
        Function to remove Arabic diacritical marks from the text.
        
        Args:
        text (str): Input string containing Arabic diacritics.
        
        Returns:
        str: The text with Arabic diacritics removed.
        """
        # Use regex substitution to replace all occurrences of Arabic diacritic marks
        # with an empty string (i.e., removing them)
        text = re.sub(self.arabic_diacritics, '', text)
        
        # Return the cleaned text without diacritics
        return text


    def remove_links(self, text: str) -> str:
        """
        Function to remove URLs (links) from the given text.

        Args:
        text (str): Input string that may contain URLs.

        Returns:
        str: The cleaned text with all URLs removed.
        """
        # Use regex to find and replace all web links starting with "http", "https" or "www"
        # \S+ matches any non-whitespace characters following the URL structure
        return re.sub("(http\S+)", "", text)

    def remove_emails(self, text: str) -> str:
        """
        Function to remove email addresses from the given text.

        Args:
        text (str): Input string that may contain email addresses.

        Returns:
        str: The cleaned text with all email addresses removed.
        """
        # Regular expression pattern for matching email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Replacing email addresses with an empty string
        cleaned_text = re.sub(email_pattern, '', text)
        
        return cleaned_text

    def remove_phone_numbers(self, text: str) -> str:
        """
        Function to remove Iranian phone numbers from the given text.

        Args:
        text (str): Input string that may contain phone numbers.

        Returns:
        str: The cleaned text with all Iranian phone numbers removed.
        """
        # Regular expression pattern:
        # - (\+98|0)? checks if the number starts with +98 (Iran country code) or 0.
        # - 9\d{9} ensures that the number follows the Iranian mobile number pattern (9 followed by 9 digits).
        # - \b ensures we match whole numbers, not part of a larger string.
        return re.sub(r"\b(\+98|0)?9\d{9}\b", "", text)

    def remove_informal_words(self, text: str) -> str:
        """
        Function to remove informal and colloquial words from the text based on a predefined list.

        Args:
        text (str): Input string containing informal words.

        Returns:
        str: The cleaned text with informal words removed.
        """

        
        # Loop through each informal word/phrase and remove it using regex substitution
        # The \b ensures that only whole words are removed (not partial matches)
        for word in self.informal_words:
            text = re.sub(word, '', text)
        
        # After all informal words are removed, return the cleaned text
        return text.strip()  # Strip any leading or trailing spaces
    
    def remove_mentions(self, text : str) -> str:
        # Regular expression to remove mentions (e.g., @username)
        return re.sub(r'@\w+', '', text)
    
    def remove_hashtags(self, text : str) -> str:
        # Regular expression to remove hashtags (e.g., #hashtag)
        return re.sub(r'#\w+', '', text)


    def remove_stopwords(self, text : str) -> str:
        """
        Function to remove stopwords from the text using Hazm's stopword list.

        Args:
        text (str): Input string containing words to filter.

        Returns:
        str: The cleaned text without stopwords.
        """
        # Tokenize the text into individual words
        words = word_tokenize(text)  # Hazm tokenizer for Persian text
        
        # Filter out words that are in the stopwords list
        filtered_words = [word for word in words if word not in self.stop_words]
        
        # Return the filtered text by joining the words back together
        return ' '.join(filtered_words)
    
    def remove_extra_spaces(self, text: str) -> str:
        """
        Function to remove extra spaces from the given text.

        Args:
        text (str): Input string that may contain multiple spaces.

        Returns:
        str: The cleaned text with extra spaces removed.
        """
        # Use regex to replace multiple spaces with a single space.
        # \s+ matches one or more whitespace characters (spaces, tabs, newlines).
        # strip() removes any leading or trailing spaces.
        return re.sub(r"\s+", " ", text).strip()

    def remove_emoji(self, text: str, replacement="") -> str:
        """
        Function to replace all emojis in the given text with a specified replacement string.

        Args:
        text (str): Input string that may contain emojis.
        replacement (str): The string that will replace the emojis. Defaults to an empty string.

        Returns:
        str: The cleaned text with all emojis replaced by the specified replacement string.
        """
        # The emoji.replace_emoji() function from the emoji library will replace all emoji characters
        # in the input text with the specified replacement string. If no replacement is provided,
        # it defaults to an empty string, effectively removing the emojis.
        return emoji.replace_emoji(text, replacement)


    def remove_not_corrected_spell(self, text : str) -> str:
        """
        Use DadmaTools to perform spell checking on the input text.

        Args:
            text (str): Input text to be spell-checked.

        Returns:
            str: Corrected text if errors are found; otherwise, the original text.
        """
        # Use DadmaTools spell checker to correct the text
        corrected_text = str(self.spell_checker(text)["spellchecker"]["corrected"])

        return corrected_text
    

# Example usage
# cleaner = CleanText()

# sample_text = """
#         :🔑من میخوام برم اینجا! این وبسایت https://example.com برای شما مفید است. ایمیل من: alireza@gmail.com شماره من: 09123456789 #alireza @metion_it
#         """
# text_no_links = cleaner.remove_links(sample_text)
# text_no_emails = cleaner.remove_emails(text_no_links)
# text_no_hashtag = cleaner.remove_hashtags(text_no_emails)
# text_no_mention = cleaner.remove_mentions(text_no_hashtag)
# text_no_phone_numbers = cleaner.remove_phone_numbers(text_no_mention)
# text_no_punc = cleaner.remove_persian_punctuation(text_no_phone_numbers)
# text_no_diacritics = cleaner.remove_arabic_diacritics(text_no_punc)
# text_no_informal = cleaner.remove_informal_words(text_no_diacritics)
# text_no_stopwords = cleaner.remove_stopwords(text_no_informal)
# text_no_extra_spaces = cleaner.remove_extra_spaces(text_no_stopwords)
# corrected_text = cleaner.remove_emoji(text_no_extra_spaces, replacement="")

# # Print final result
# print("Final Cleaned Text:", corrected_text)

#output

    # Final Cleaned Text: من برم وبسایت مفید ایمیل شماره