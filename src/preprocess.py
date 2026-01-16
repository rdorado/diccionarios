import sys
import re
import os

preprocitions = [ 'a', 'á', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde',
                  'durante', 'en', 'entre', 'hacia', 'hasta', 'mediante',
                  'para', 'por', 'según', 'sin', 'so', 'sobre', 'tras',
                  'versus', 'vía' ]


pronouns = [ 'yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros', 'ellos',
             'me', 'te', 'se', 'nos', 'os', 'le', 'les' ]

determiners = [ 'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
                'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos',
                'esas', 'aquel', 'aquella', 'aquellos', 'aquellas',
                'mi', 'mis', 'tu', 'tus', 'su', 'sus', 'nuestro',
                'nuestra', 'nuestros', 'nuestras', 'vuestro',
                'vuestra', 'vuestros', 'vuestras' ]

conjunctions = [ 'y', 'e', 'ni', 'o', 'u', 'pero', 'mas', 'sino',
                 'aunque', 'porque', 'pues', 'que' ]

contractions = [ "al", "del" ]

"""
auxiliary_verbs_ser = [ 'soy', 'eres', 'es', 'somos', 'sois', 'son',
                     'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron',
                     'siendo', 'sido' , 'seré', 'serás', 'será', 'seremos',
                     'seréis', 'serán', 'sería', 'serías', 'sería', 'seríamos',
                     'seríais', 'serían', 'era', 'eras', 'era', 'éramos',
                     'erais', 'eran' ]

auxiliary_verbs = auxiliary_verbs_ser
"""

stopwords = preprocitions + pronouns + determiners + conjunctions + contractions

def replace_punctuation(word):
    """
    Clean the input text by removing punctuation and special characters.
    
    Args:
        text: Input text string to clean
    Returns:
        Cleaned text string
    """
    word = re.sub(r'[^a-zA-Záéíóúüñ]', ' ', word)
    return re.sub(r'  +', ' ', word).strip()

def process_file(input_path, output_path):
    """
    Process a file and count word occurrences.
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        Dictionary with words as keys and counts as values
    """ 
    try:
        with open(input_path, 'r', encoding='utf-8') as input_file, open(output_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                line = line.lower()
                line = re.sub(r'[^a-zA-Záéíóúüñ:;,.¿¡?!]', ' ', line)
                line = line.replace(':', ' : ')
                line = line.replace(';', ' ; ')
                line = line.replace('.', ' . ')
                line = line.replace(',', ' , ')
                line = line.replace('¿', ' ¿ ')
                line = line.replace('?', ' ? ')
                line = line.replace('¡', ' ¡ ')
                line = line.replace('!', ' ! ')
                line = re.sub(r'  +', ' ', line).strip()
                
                output_file.write(line+ '\n')
    except Exception as e:
        print(f"Error processing file {input_path}: {e}")



def main():

    if len(sys.argv) < 2:
        sys.exit(1)

    command = sys.argv[1]

    if command == "preprocess":
        if len(sys.argv) != 4:
            print("Usage: python preprocess.py preprocess <input_file> <output_file>")
            sys.exit(1)

        input_file = sys.argv[2]
        output_file = sys.argv[3]

        print(f"Preprocessing file: {input_file}")
        print(f"Preprocessed data saved to: {output_file}")
        process_file(input_file, output_file)

    elif command == "preprocess-batch":
        if len(sys.argv) != 4:
            print("Usage: python preprocess.py preprocess-batch <input_directory> <output_directory>")
            sys.exit(1)

        input_directory = sys.argv[2]
        output_directory = sys.argv[3]

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for filename in os.listdir(input_directory):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)

            print(f"Preprocessing file: {input_path}")
            process_file(input_path, output_path)
            print(f"Preprocessed data saved to: {output_path}")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()