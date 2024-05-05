# Imports
import re
import itertools
import roman

# TODOs:
# - Remove accents to mono-syllabic words
# - lo enʌiendeь → lo'nʌiendeь
# - eьʌoi → eьʌói
# Бuelʌa a Eьpaña → Бuelʌa'Ьpaña
# Keep «para» (verb) 

# Create Conversor class
class AndalusianConversor:

    def __init__(self, 
                 rotacism: bool = False):
        """
        Initializes the class with the necessary parameters.

        Parameters:
        - rotacism (bool): whether to apply rotacism (transformation of /l/ into /r/ before consonants).
                           Default is False.
        """
        ### Sets ###
        self.NON_ACCENTED_VOWELS = 'aeiouAEIOUÜ'
        self.ACCENTED_VOWELS = 'áéíóúÁÉÍÓÚ'
        self.VOWELS = self.NON_ACCENTED_VOWELS + self.ACCENTED_VOWELS

        self.ORIGINAL_CONSONANTS = 'bcdfghjklmnñpqrstvwxyzBCDFGHJKLMNÑPQRSTVWXYZ'
        self.NEW_CONSONANTS = 'ʌъƨьɿзбɅЪƧЬႨЗГБ'
        self.CONSONANTS = self.ORIGINAL_CONSONANTS + self.NEW_CONSONANTS

        self.LETTERS = self.VOWELS + self.CONSONANTS
        self.STOPCHARS = '.,:;?!¡¿ $\(\)\[\]\{\}«»\'\"'

        ### Conversions ###
        # Accents
        self.TO_ACCENTED_VOWEL = {
            'a': 'á',
            'e': 'é',
            'i': 'í',
            'o': 'ó',
            'u': 'ú',
            'A': 'Á',
            'E': 'É',
            'I': 'Í',
            'O': 'Ó',
            'U': 'Ú',
        }

        self.TO_NON_ACCENTED_VOWEL = {v: k for k, v in self.TO_ACCENTED_VOWEL.items()}

        # Uppercasing and lowercasing
        self.UPPERCASE = {
            'a' : 'A',
            'б' : 'Б',
            'c' : 'C',
            'd' : 'D',
            'e' : 'E',
            'f' : 'F',
            'ƨ' : 'Ƨ',
            'ь' : 'Ь',
            'i' : 'I',
            'l' : 'L',
            'm' : 'M',
            'n' : 'N',
            'o' : 'O',
            'p' : 'P',
            'r' : 'Γ',
            'ъ' : 'Ъ',
            'ʌ' : 'Ʌ',
            'u' : 'U',
            'w' : 'W',
            'y' : 'Y',
            'ч' : 'Ч',
            'ɿ' : 'Ⴈ'
        }

        self.LOWERCASE = {v: k for k, v in self.UPPERCASE.items()}

        # Measurement abbreviations
        self.MEASUREMENT_ABBREVIATIONS = {
            # Time
            's' : 'ъ',
            'm' : 'm',
            'h' : 'o',
            # Distance
            'mm' : 'mm',
            'cm' : 'ɿm',
            'dm' : 'dm',
            # 'm' : 'm', # Duplicated with minutes
            'Dm' : 'Dm',
            'hm' : 'em',
            'km' : 'cm',
            # Litres
            'ml' : 'll',
            'cl' : 'ɿl',
            'dl' : 'dl',
            'l' : 'l',
            'Dl' : 'Dl',
            'hl' : 'el',
            'kl' : 'cl',
        }

        ### Flags ###
        self.rotacism = rotacism

    ### Methods ###
        
    def show_text(self):
        """
        Formats the text for ease of use
        """

        lines = self.text.split(', ')
        for line in lines:
            print(line.strip())


    ### Step 0: preprocessing ###
        
    def clean_text(self):
        """
        Applies basic preliminary cleanings to the text. Including the following:
        - Remove phantom separation occurring in Wikipedia articles when two references are next to each other.
        - Remove numbers after a word.
        """

        # Remove phantom spaces
        self.text = self.text.replace('​', '')

        # Remove numbers after a word
        pattern = r'([a-zA-Z]+)\d+'
        output = r'\1'
        self.text = re.sub(pattern, output, self.text)
    

    ### Step 1: direct replacements ###
                
    def apply_direct_replacements(self):
        """
        Modifies directly certain expressions.
        """

        direct_replacements = {
            # Standard Spanish : Andalusian Spanish
            f'([{self.STOPCHARS}])para([{self.STOPCHARS}])' : r'\1pa\2',
            f'([{self.STOPCHARS}])Para([{self.STOPCHARS}])' : r'\1Pa\2',
            f'([{self.STOPCHARS}])muy([{self.STOPCHARS}])' : r'\1mu\2',
            f'([{self.STOPCHARS}])Muy([{self.STOPCHARS}])' : r'\1Mu\2',
            f'([{self.STOPCHARS}])todo([{self.STOPCHARS}])' : r'\1ʌo\2',
            f'([{self.STOPCHARS}])Todo([{self.STOPCHARS}])' : r'\1Ʌo\2',
            f'([{self.STOPCHARS}])toda([{self.STOPCHARS}])' : r'\1ʌoa\2',
            f'([{self.STOPCHARS}])Toda([{self.STOPCHARS}])' : r'\1Ʌoa\2',
            f'([{self.STOPCHARS}])todos([{self.STOPCHARS}])' : r'\1ʌoь\2',
            f'([{self.STOPCHARS}])Todos([{self.STOPCHARS}])' : r'\1Ʌoь\2',
            f'([{self.STOPCHARS}])todas([{self.STOPCHARS}])' : r'\1ʌoaь\2',
            f'([{self.STOPCHARS}])Todas([{self.STOPCHARS}])' : r'\1Ʌoaь\2',
            f'([{self.STOPCHARS}])pues([{self.STOPCHARS}])' : r'\1poь\2',
            f'([{self.STOPCHARS}])Pues([{self.STOPCHARS}])' : r'\1Poь\2',
            f'([{self.STOPCHARS}])etc([{self.STOPCHARS}])' : r'\1eьɿ\2',
        }

        # Loop through the dictionary
        for key, value in direct_replacements.items():
            self.text = re.sub(key, value, self.text)


    def replace_roman_numerals(self):
        """
        Replaces roman numerals with arabic numerals. 
        It is assumed that all instances of roman numerals are in the form "siglo " + roman numeral
        or "siglos " + roman numeral.
        """

        # Find instances of "siglo " + roman numerals
        # Replace by patterns, Longer patterns first
        roman_patterns = [
            (rf'siglos? [ivxlcdmIVXLCDM]+ y ([ivxlcdmIVXLCDM]+)[{self.STOPCHARS}]', f'siglos? [ivxlcdmIVXLCDM]+ y [ivxlcdmIVXLCDM]+[{self.STOPCHARS}]'),
            (rf'siglos? ([ivxlcdmIVXLCDM]+)[{self.STOPCHARS}]', rf'siglos? [ivxlcdmIVXLCDM]+[{self.STOPCHARS}]')
        ]

        # If there are any, extract the roman numerals and convert them to arabic
        siglo_relaces = {}
        for pattern, clean_pattern in roman_patterns:    
            siglos = re.findall(clean_pattern, self.text)
            for siglo in siglos:
                # Extract the roman numerals
                has_pattern = re.match(pattern, siglo) is not None
                if has_pattern:
                    roman_numeral = re.match(pattern, siglo).group(1)
                    arabic_numeral = roman.fromRoman(roman_numeral.upper())
                    # Replace the roman numerals with the arabic numerals
                    siglo_relaces[siglo] = siglo.replace(roman_numeral, str(arabic_numeral))

        # Loop through the dictionary
        for key, value in siglo_relaces.items():
            self.text = self.text.replace(key, value)

    
    ### Step 2: contextual replacements ###
            
    def apply_contextual_conversions(self):
        """
        Applies conself.textual conversions to the self.text.

        Some letters depend on the conself.text to be transformed. This implies that order matters.

        * x
            * If it is at the beginning of a word, it is transformed into "ъ".
            * If it is at the end of a word, it is transformed into "ь".
            * If it is enclosed between two vowels, it is transformed into "ьъ".
            * Otherwise, it is transformed into "ь".

        * g
            * If followed by "e" or "i", it is transformed into "ь".
            * Otherwise, it is transformed into "ƨ".

        * c
            * If followed by "e" or "i", it is transformed into "ɿ".
            * Otherwise, it is transformed into "c".
        """

        CONTEXTUAL_CONVERSIONS = {
            ### g
            # Lowercase
            'g([eiéí])' : r'ь\1',
            'gu([eiéí])' : r'ƨ\1',
            'gü' : 'w',
            'g([aoáó])' : r'ƨ\1',
            'gu([aoáó])' : r'w\1',
            # Uppercase
            'G([eiEIéíÉÍ])' : r'Ь\1',
            'Gu([eiEIéíÉÍ])' : r'Ƨ\1',
            'G[üÜ]' : 'W',
            'G([aoAOáóÁÓ])' : r'Ƨ\1',
            'Gu([aoAOáóÁÓ])' : r'W\1',

            ### c
            # Lowercase
            'c([eiéíEIÉÍ])' : r'ɿ\1',
            # Uppercase
            'C([eiéíEIÉÍ])' : r'Ⴈ\1',

            ### x
            # Lowercase
            f'([{self.VOWELS}])x([{self.VOWELS}])' : r'\1ьъ\2',
            f'x([{self.CONSONANTS}])' : r'ь\1',
            # f'x([{stopchars}])' : r'ь\1', # Special case to be handled in word-end transformations
            f'([{self.VOWELS}])X([{self.VOWELS}])' : r'\1ЬЪ\2',
            f'X([{self.CONSONANTS}])' : r'Ь\1',
            # f'X([{stopchars}])' : r'Ь\1', # Special case to be handled in word-end transformations

            ### y
            # Lowercase
            f'([{self.VOWELS}{self.STOPCHARS}])y([{self.CONSONANTS}{self.STOPCHARS}])' : r'\1i\2',
            # Uppercase
            f'([{self.VOWELS}{self.STOPCHARS}])Y([{self.CONSONANTS}{self.STOPCHARS}])' : r'\1I\2',
        }

        # Loop through the dictionary
        for key, value in CONTEXTUAL_CONVERSIONS.items():
            self.text = re.sub(key, value, self.text)

    
    ### Step 3: direct conversions ###
    
    def apply_direct_conversions(self):
        """
        Applies direct conversions to the self.text.

        The following letters can always be converted to the same letter in Andalusian, **regardless of the conself.text**:

        | Letter | Translit. |
        |--------|-----------|
        | b      | б         |
        | v      | б         |
        | k      | c         |
        | qu     | c         |
        | t      | ʌ         |
        | ll     | y         |
        | s      | ъ         |
        | j      | ь         |
        | z      | ɿ         |
        | ch     | ч         |
        | h      |           |
        """

        # Dictionary of direct conversions
        DIRECT_CONVERSIONS = {
        'b' : 'б',
        'B' : 'Б',
        'v' : 'б',
        'V' : 'Б',
        'g' : 'ƨ',
        'G' : 'Ƨ',
        'k' : 'c',
        'K' : 'C',
        'qu' : 'c',
        'Qu' : 'C',
        't' : 'ʌ',
        'T' : 'Ʌ',
        'll' : 'y',
        'Ll' : 'Y',
        's' : 'ъ',
        'S' : 'Ъ',
        'j' : 'ь',
        'J' : 'Ь',
        'z' : 'ɿ',
        'Z' : 'Ⴈ',
        'ch' : 'ч',
        'Ch' : 'Ч',
        'h' : '',
        'R' : 'Γ'
        }

        # Create a regular expression that matches any key in the dictionary
        regex = re.compile("(%s)" % "|".join(map(re.escape, DIRECT_CONVERSIONS.keys())))

        # Replace the matches with the values in the dictionary
        self.text = regex.sub(lambda x: DIRECT_CONVERSIONS[x.group(0)], self.text)
    

    def capitalize_post_h_consonants(self):
        """
        Capitalizes the second letter of all instances of "H" followed by a consonant.
        """

        # Find all H instances
        capital_h = re.findall('H.', self.text)

        # Loop through the list creating replaces where the H is replaced by the second letter capitalized
        replaces = {combination : combination.upper()[1] for combination in capital_h}
        for key, value in replaces.items():
            self.text = self.text.replace(key, value)

    ### Step 4: word-end transformations ###
            
    # Auxiliar methods
    def detach_stopchars(self,
                         word: str):
        """Separates the stopchars from the word and returns both separately"""

        # If there are no stopchars, return the word as is and None
        if not re.search(f'[{self.STOPCHARS}]$', word):
            return word, None
        
        # Otherwise, detach stopchars from the word if they are present
        else:
            word_stopchars = re.findall(f'([{self.STOPCHARS}]+)$', word)
            assert len(word_stopchars) == 1, f'Unexpected number of stopchars found: {word_stopchars} for word {word}'
            word_stopchars = word_stopchars[-1]
            word = re.sub(f'([{self.STOPCHARS}]+)$', '', word)

            return word, word_stopchars
        
    
    def remove_final_consontants(self,
                                 word: str) -> str:
        """Removes final consonants from a word if they are present."""

        # Remove consonants at the end of the word if they are present
        end_consonants = re.findall(f'([{self.CONSONANTS}]+)$', word)
        if end_consonants:
            # Remove the consonants
            word = re.sub(f'([{self.CONSONANTS}]+)$', '', word)
        
        return word
    

    def add_accent_mark(self,
                        word: str) -> str:
        """
        Adds an accent mark to the last vowel of a word if necessary.
        """

        # Remove consonants at the end of the word if they are present
        end_consonants = re.findall(f'([{self.CONSONANTS}]+)$', word)
        if end_consonants:
            # Remove the consonants
            word = re.sub(f'([{self.CONSONANTS}]+)$', '', word)    

            # Add an accent mark to the last vowel
            try:
                last_letter = word[-1]    
            # In some cases, i.e., abbreviatures (cm), the whole word can be deleted.
            # If it happens, return the raw word
            except IndexError: 
                return word
            
            # Check if the remaining last character is a vowel
            # If not, it might be a model name, a unit of measure or a special character like "'"
            # In this case, return the word as is.
            last_char_check = re.search(f'[{self.VOWELS}]$', word) is not None
            if not last_char_check:
                return word

            assert last_letter in self.VOWELS, f'Unexpected last letter of word: {word[-1]} for word {word}'
            word_root = word[:-1]
            marked_letter = self.TO_ACCENTED_VOWEL[last_letter]
            word = word_root + marked_letter

        return word
    

    def remove_accent_mark(self,
                           word: str) -> str:
        """
        Removes an accent mark from the last valid vowel of a word if necessary.
        """

        # Find all accented vowels
        aux_accented = re.findall(f"[{self.ACCENTED_VOWELS}]", word)

        # If there are no accented vowels, return the word as is
        if not aux_accented:
            return word
        
        # If there are accented vowels, replace them with their non-accented counterparts
        for accented_vowel in set(aux_accented):
            word = word.replace(accented_vowel, self.TO_NON_ACCENTED_VOWEL[accented_vowel])

        return word

    
    def handle_d_endings(self,
                         word: str) -> str:
        """
        Handles the -d- ending in words.
        """

        # If the word is stressed in the third-to-last syllable,
        # no changes are necessary
        aux_mask = (
            re.search(rf'[{self.NON_ACCENTED_VOWELS}]d[oa]ь?$', word) is not None and
            re.search(f'[{self.ACCENTED_VOWELS}]', word) is not None
        )
        if aux_mask: 
            return word
        
        # In other cases, drop intervocalic -d- in the last syllable and manage accents
        pattern = rf'([aeiuáéíúAEIUÁÉÍÚ])d([oóa])(ь)?$'
        output = rf'\1\2\3'
        word = re.sub(pattern, output, word)

        # Handle accents
        aux_accent_dict  = {
            'ao(ь)?$' : r'áo\1',
            'aa(ь)?$' : r'á\1',
            'i([ao])(ь)?$' : r'í\1\2',
            'u([ao])(ь)?$' : r'ú\1\2'
        }
        for pattern, output in aux_accent_dict.items():
            if re.search(pattern, word) is not None:
                word = re.sub(pattern, output, word)
                break

        return word 
    

    def perform_word_end_transformations(self,
                                         word: str) -> str:
        """
        Wrapper function to perform changes at the end of words,
        managing also accent marks.
        """

        # Determine sets
        second_to_last_accented_consonants = 'ʌdpбcƨfrl'
        last_accented_consonants = 'ɿm'
        word_end_transformations = {
            'ъ' : {'pattern' : rf'ъ([{self.STOPCHARS}]+)?$', 'output' : r'ь\1'},
            'ɿ' : {'pattern' : rf'ɿ([{self.STOPCHARS}]+)?$', 'output' : r'ь\1'},
            'm' : {'pattern' : rf'm([{self.STOPCHARS}]+)?$', 'output' : r'n\1'},
        }

        # Set words that remain unchanged
        INMUTABLE_EXCEPTIONS = ['el', 'del', 'al', 'por', 'eьɿ']
        INMUTABLE_EXCEPTIONS.extend([word.capitalize() for word in INMUTABLE_EXCEPTIONS])

        # Detect last letter to perform the appropriate transformation
        original_word = word
        word, word_stopchars = self.detach_stopchars(word)
    
        # Some stopchars combinations (e.g. (...)) or inmutable exceptions with stopwords can get here 
        # If it happens, return the word as is
        if word == '' or word in INMUTABLE_EXCEPTIONS:
            return original_word
        # Otherwise, get the last letter
        else:
            last_letter = word[-1]

        ### Handle special cases ###
        
        # Skip inmutable words or words with just one character
        if word in INMUTABLE_EXCEPTIONS or len(word) == 1:
            if word_stopchars: # Attach stopchars if they are present
                word += word_stopchars            
            return word
        
        # Units of measure should remain unchanged
        if word in self.MEASUREMENT_ABBREVIATIONS.values():
            if word_stopchars: # Attach stopchars if they are present
                word += word_stopchars
            return word

        # Check if the word has an accent mark
        has_accent = re.search(f'[{self.ACCENTED_VOWELS}]', word) is not None

        ### Handle last consonant cases ###

        # Handle special cases first
        # -x
        if last_letter in 'xX':
            if has_accent:
                word = self.remove_accent_mark(word)
            else:
                word = self.add_accent_mark(word)
                
            word = re.sub('x$', 'ь', word)
            word = re.sub('X$', 'Ь', word)

        # -pъ
        elif word[-2:].lower() == 'pъ':
            if has_accent:
                word = self.remove_accent_mark(word)
            else:
                word = self.add_accent_mark(word)
                
            word = re.sub('pъ$', 'ь', word)
            word = re.sub('PЪ$', 'Ь', word)

        # Words with second to last accented consonants
        elif last_letter in second_to_last_accented_consonants:
            if has_accent:
                word = self.remove_accent_mark(word)
            else:
                word = self.add_accent_mark(word)
                
            word = self.remove_final_consontants(word)
        
        # Words with last accented consonants
        elif last_letter in last_accented_consonants:
            if has_accent:
                word = self.remove_accent_mark(word)
                pattern = word_end_transformations[last_letter]['pattern']
                output = word_end_transformations[last_letter]['output']
                word.replace(pattern, output)
            else:
                word = self.add_accent_mark(word)
                transformed_ending = word_end_transformations[last_letter]['output'].replace(r'\1', '')
                word += transformed_ending

        # Special case for 'ъ': the accent rules do not change
        elif last_letter == 'ъ':
            pattern = word_end_transformations[last_letter]['pattern']
            output = word_end_transformations[last_letter]['output']
            word = re.sub(pattern, output, word)

        # Handle -d- endings
        if re.search(f'[{self.VOWELS}]d[{self.VOWELS}{self.ACCENTED_VOWELS}]ь?', word) is not None:
            word = self.handle_d_endings(word)

        # Attach stopchars from the word if they are present
        if word_stopchars:
            word += word_stopchars
        
        return word
    
    def word_end_transformation_wrapper(self):
        """
        Wrapper function to perform word-end transformations.
        """

        # Split the text into words, apply the transformations and join them back.
        lines = self.text.strip().split('\n')
        processed_text = ''
        for line in lines:
            # Split, transform and join the words
            words = line.split(' ')
            words = [self.perform_word_end_transformations(word) for word in words if word != '' and word not in self.STOPCHARS]    
            words = ' '.join(words)

            # Add it back to the text
            processed_text += words + '\n'

            # Set it back to the text
            self.text = processed_text

        # Remove the last newline character
        self.text = self.text[:-1]


    ### Step 5: word initial transformations ###
            
    def apply_initial_transformations(self):
        """
        Applies initial transformations to the text.
        """

        # Dictionary of initial transformations
        WORD_INITIAL_TRANSFORMATIONS = {
            f'([^{self.LETTERS}])pъ([{self.LETTERS}])' : r'\1ъ\2',
            f'([^{self.LETTERS}])Pъ([{self.LETTERS}])' : r'\1Ъ\2',
            f'([^{self.LETTERS}])mn([{self.LETTERS}])' : r'\1n\2',
            f'([^{self.LETTERS}])Mn([{self.LETTERS}])' : r'\1N\2',
            f'([^{self.LETTERS}])u([eiéí])([{self.LETTERS}])' : r'\1w\2\3',
            f'([^{self.LETTERS}])U([eiéíEIÉÍ])([{self.LETTERS}])' : r'\1W\2\3',
            
        }

        # Loop through the dictionary
        for key, value in WORD_INITIAL_TRANSFORMATIONS.items():
            self.text = re.sub(key, value, self.text)
    

    ### Step 6: internal word transformations ###
            
    def apply_r_transformations(self):
        """
        Substitutes 'r' with 'n' or 'l' depending on the context.
        """

        # 'r'-substitutions
        R_SUBSTITUTION = {'pattern' : r'r([ln])', 'output' : r'\1\1'}
        self.text = re.sub(R_SUBSTITUTION['pattern'], R_SUBSTITUTION['output'], self.text)


    def simplify_consonant_clusters(self):
        """
        Simplifies three-letter consonant clusters.
        """

        CONSONANT_CLUSTERS_REPLACES = {
            f'([{self.VOWELS}])[бn]ъ([{self.CONSONANTS}])' : r'\1ь\2'
            }

        # Loop through the dictionary
        for key, value in CONSONANT_CLUSTERS_REPLACES.items():
            self.text = re.sub(key, value, self.text)

    
    def apply_reductor_collisions(self):
        """
        Reductors are a set of consonants that, when grouped together, the first one is reduced to 'ь'. 
        """

        # Reductor colisions
        REDUCTORS = 'cƨʌdьъɿpбf'
        REDUCTOR_COMBINATIONS = [''.join(pair) for pair in itertools.permutations(REDUCTORS, 2)]
        REDUCTOR_REPLACES = {pair : 'ь' + pair[1] for pair in REDUCTOR_COMBINATIONS}

        # Loop through the dictionary
        for key, value in REDUCTOR_REPLACES.items():
            self.text = re.sub(key, value, self.text)

        # 'n' acts as a reductor when placed after another reductor, but it is immune to this process
        self.text = re.sub(f'[{REDUCTORS}]n', r'ьn', self.text)

    
    def apply_other_simplifications(self):
        """
        Applies other specific simpifications changes to the text.
        """

        OTHER_SIMPLIFICATIONS = {
            'nб' : 'mб',
            'ee' : 'e',
            'nm' : 'mm',
        }

        for key, value in OTHER_SIMPLIFICATIONS.items():
            self.text = self.text.replace(key, value)

    
    ### Step 7: weak particles assimilation ###
            
    def apply_weak_particles_assimilation(self):
        """
        Several common use particles loose their vowels and are attached to nearby words, forming contractions.
        """

        assimilations_dict = {
            f'([{self.STOPCHARS}])([dʌъlm])e ([{self.VOWELS}])' : r"\1\2'\3",
            f'([{self.STOPCHARS}])([DɅЪLM])e ([{self.VOWELS}])' : r"\1\2'\3",
            f'([{self.STOPCHARS}])c[eé] ([{self.VOWELS}])' : r"\1c'\2",
            f'([{self.STOPCHARS}])C[eé] ([{self.VOWELS}])' : r"\1C'\2",
            f'([{self.STOPCHARS}])la a' : r"\1l'a",
            f'([{self.STOPCHARS}])La a' : r"\1L'a",
            f'([{self.STOPCHARS}])lo o' : r"\1l'o",
            f'([{self.STOPCHARS}])Lo o' : r"\1L'o",
            f'([aeoáéó]) e([ln])([{self.STOPCHARS}])' : r"\1'\2\3", # NOTE: review
            f'([{self.VOWELS}]) e([{self.CONSONANTS}]{2,})' : r"\1'\2", # NOTE: review
            f'o ([oóOÓ])' : r"'\1",
        }

        for key, value in assimilations_dict.items():
            self.text = re.sub(key, value, self.text)

    
    ### Step 8: rotacism ###
            
    def apply_rotacism(self):
        """
        'l' before 'r' can convert to 'r' before consonants in some speakers.
        This function applies rotacism to the text.
        """

        # Lowercase
        pattern = f'l( ?)([{self.CONSONANTS}])'
        output = r'r\1\2'
        self.text = re.sub(pattern, output, self.text)

        # Uppercase
        pattern = f'L( ?)([{self.CONSONANTS}])'
        output = r'Γ\1'
        self.text = re.sub(pattern, output, self.text)

    ### Step 9: space-separated 'r' assimilation
        
    def apply_space_separated_r_assimilation(self):
        """
        If a word preserves a final 'r' and the next word starts with 'l' or 'n', the 'r' is assimilated.
        """

        # Apply space-separated "r" assimilation
        SPACE_SEPARATED_R_PATTERN = 'r ([lnLN])'
        output = r'\1 \1'
        self.text = re.sub(SPACE_SEPARATED_R_PATTERN, output, self.text)

    ### Main method ###
    def convert(self, text):
        """
        Applies all the transformations to the text.
        """
        self.original_text = text
        self.text = text

        # Step 0: preprocessing
        self.clean_text()

        # Step 1: direct replacements
        self.apply_direct_replacements()
        self.replace_roman_numerals()

        # Step 2: contextual replacements
        self.apply_contextual_conversions()

        # Step 3: direct conversions
        self.apply_direct_conversions()
        self.capitalize_post_h_consonants()

        # Step 4: word-end transformations
        self.word_end_transformation_wrapper()

        # Step 5: word initial transformations
        self.apply_initial_transformations()

        # Step 6: internal word transformations
        self.apply_r_transformations()
        self.simplify_consonant_clusters()
        self.apply_reductor_collisions()
        self.apply_other_simplifications()

        # Step 7: weak particles assimilation
        self.apply_weak_particles_assimilation()

        # Step 8: rotacism
        if self.rotacism:
            self.apply_rotacism()

        # Step 9: space-separated 'r' assimilation
        self.apply_space_separated_r_assimilation()

        return self.text
