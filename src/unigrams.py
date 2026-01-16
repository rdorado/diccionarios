import sys
import os

from preprocess import replace_punctuation, stopwords

def help():
    print("Usage: python unigrams.py <command>")
    print("List of commands:")
    print("  create <input_file> [output_file]")

def process_file(file_path):
    """
    Process a file and count word occurrences.
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        Dictionary with words as keys and counts as values
    """
    word_count = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                candidates = line.lower().split()
                for candidate in candidates:
                    # Remove punctuation if needed
                    
                    #translator = str.maketrans('', '', string.punctuation)
                    #word = word.translate(translator)
                    
                    #word = word.strip('.,¡!¿?;:-"\'()[]	_$1234567890%*&^#@`~«»•“”‘’')
                    clean_candidate = replace_punctuation(candidate)
                    tokens = clean_candidate.strip().split()
                    for word in tokens:
                        if word:
                            word_count[word] = word_count.get(word, 0) + 1
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {}
    
    return word_count

def read_unigrams(file_path):
    """
    Read a dictionary file and return a word count dictionary.
    
    Args:
        file_path: Path to the dictionary file
    Returns:
        Dictionary with words as keys and counts as values
    """
    word_count = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word, count = parts
                word_count[word] = int(count)
                
    
    return word_count

def write_unigrams(file_path, unigrams, threshold=0):
    with open(file_path, 'w', encoding='utf-8') as out_f:
        for word, count in sorted(unigrams.items()):
            if count >= threshold:
                out_f.write(f"{word}\t{count}\n")

def print_filtered(dictionary, minthreshold, maxthreshold, skip_stopwords=False):
    for word, count in dictionary.items():
        if skip_stopwords and word in stopwords:
            continue
        if count >= minthreshold and count <= maxthreshold:
            print(f"'{word}'\t{count}")

def calculate_N(dictionary):
    """
    Calculate the total count of words in the dictionary.
    
    Args:
        dictionary: Dictionary with words as keys and counts as values
        
    Returns:
        Total count of words
    """
    total = sum(dictionary.values())
    return total

def main():

    if len(sys.argv) < 2:

        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 5:
            print("Usage: python makedict.py create <input_files> <output_file> threshold")
            sys.exit(1)

        input_file = sys.argv[2]
        result = None
        if not os.path.exists(input_file):
            print(f"File {input_file} does not exist. Skipping.")
        else:
            print(f"Processing input file: {input_file}")
            result = process_file(input_file)

        output_file = sys.argv[-2]
        threshold = int(sys.argv[-1])
        if result is not None:
            try:
                write_unigrams(output_file, result, threshold)
                print(f"Dictionary written to {output_file}")
            except Exception as e:
                print(f"Error writing to output file {output_file}: {e}")

        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")

    elif command == "create-batch":
        if len(sys.argv) < 5:
            print("Usage: python makedict.py create-batch <input_directory> <output_file> threshold")
            sys.exit(1)

        input_directory = sys.argv[2]
        output_directory = sys.argv[3]
        threshold = int(sys.argv[-1])

        if not os.path.isdir(input_directory):
            print("Error. Provided input directory does not exist. Exiting.")
            sys.exit(1)

        if not os.path.isdir(output_directory):
            print("Error. Provided output directory does not exist. Exiting.")
            sys.exit(1)

        for f in os.listdir(input_directory):
            input_file = os.path.join(input_directory, f)
            result = None
            if os.path.isfile(input_file):
                print(f"Processing input file: {input_file}")
                result = process_file(input_file)

            if result is not None:
                output_file = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_file))[0]}.unigrams")
                try:
                    write_unigrams(output_file, result, threshold)

                    print(f"Input file: {input_file}")
                    print(f"Dictionary written to {output_file}")
                except Exception as e:
                    print(f"Error writing to output file {output_file}: {e}")

    elif command == "merge-batch":
        if len(sys.argv) < 5:
            print("Usage: python makedict.py merge-batch <input_directory> <output_file> threshold")
            sys.exit(1)

        input_directory = sys.argv[2]
        output_file = sys.argv[3]
        threshold = int(sys.argv[4])
        merged_dict = {}

        if not os.path.isdir(input_directory):
            print("Error. Provided input directory does not exist. Exiting.")
            sys.exit(1)

        output_dir = os.path.dirname(output_file)
        if not os.path.isdir(output_dir):
            print("Error. Parent directory of output file does not exist. Exiting.")
            sys.exit(1)

        for f in os.listdir(input_directory):
            dict_file = os.path.join(input_directory, f)
            if os.path.isfile(dict_file):
                try:
                    dictionary = read_unigrams(dict_file)
                    for word, count in dictionary.items():
                        merged_dict[word] = merged_dict.get(word, 0) + int(count)
                except Exception as e:
                    print(f"Error reading dictionary file {dict_file}: {e}")

            try:
                with open(output_file, 'w', encoding='utf-8') as out_f:
                    for word, count in sorted(merged_dict.items()):
                        if count >= threshold:
                            out_f.write(f"{word}\t{count}\n")
                print(f"Merged dictionary {dict_file} written to {output_file}")
            except Exception as e:
                print(f"Error writing to output file {output_file}: {e}")

    elif command == "compare":
        if len(sys.argv) < 4:
            print("Usage: python makedict.py compare <dict_file1> <dict_file2>")
            sys.exit(1)

        dict_file1 = sys.argv[2]
        dict_file2 = sys.argv[3]

        dict1 = read_unigrams(dict_file1)
        dict2 = read_unigrams(dict_file2)

        dic1N = calculate_N(dict1)
        dic2N = calculate_N(dict2)

        word_in_common = set(dict1.keys()) & set(dict2.keys())

        result = 0
        for word in sorted(word_in_common):
            result = result + min(dict1[word]/dic1N, dict2[word]/dic2N)

        print(f"Result: {result}")
    elif command == "filter":
        if len(sys.argv) != 5:
            sys.exit(1)

        input_file = sys.argv[2]
        dic = read_unigrams(input_file)

        minthreshold = int(sys.argv[3])
        maxthreshold = int(sys.argv[4])
        print_filtered(dic, minthreshold=minthreshold, maxthreshold=maxthreshold, skip_stopwords=True)
    else:
        print(f"Unknown command: {command}")
        help()
        sys.exit(1)

if __name__ == "__main__":
    main()