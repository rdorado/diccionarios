import sys
import os

from preprocess import stopwords
from bigrams import read_tagged

def tag_file(input_path, word_tags, output_path):
    """
    Tag words in the input file based on the tagged data.
    
    Args:
        input_path: Path to the input text file
        tagged_path: Path to the tagged data file
        output_path: Path to the output tagged file
    """

    try:
        with open(input_path, 'r', encoding='utf-8') as input_file, open(output_path, 'w', encoding='utf-8') as output_file:
            
            for line in input_file:
                words = line.strip().split()
                tagged = []
                for word in words:
                    if word in [":", ";", ".", ",", "!", "?", "¡", "¿"]:
                        tagged.append(word+"/"+word)
                    elif word in stopwords:
                        tagged.append(word+"/"+word.upper())
                    elif word in word_tags:
                        tagged.append(word+"/"+word_tags[word])
                    else:
                        tagged.append(word+"/UNK")  # Default tag
                output_file.write(" ".join(tagged) + "\n")

    except Exception as e:
        print(f"Error processing file {input_path}: {e}")   


def help():
    print("Usage: python analysis.py <command>")
    print("List of commands:")
    print("  ")

def main():

    command = sys.argv[1]

    if command == "tag":
        if len(sys.argv) != 5:
            sys.exit(1)

        tagged_file = sys.argv[2]
        input_file = sys.argv[3]
        output_file = sys.argv[4]

        tagged_data = read_tagged(tagged_file)
        categories = {}
        for tag, words in tagged_data.items():
            for word in words:
                categories[word] = tag

        tag_file(input_file, categories, output_file)
        
    elif command == "tag-batch":
        if len(sys.argv) != 5:
            sys.exit(1)

        tagged_file = sys.argv[2]
        input_dir = sys.argv[3]
        output_dir = sys.argv[4]

        tagged_data = read_tagged(tagged_file)
        categories = {}
        for tag, words in tagged_data.items():
            for word in words:
                categories[word] = tag
        for f in os.listdir(input_dir):
            input_path = os.path.join(input_dir, f)
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}.tagged")
            tag_file(input_path, categories, output_file)
            print(f"Tagged file written to: {output_file}")

    elif command == "merge":
        if len(sys.argv) != 4:
            sys.exit(1) 
        input_dir = sys.argv[2]
        output_file = sys.argv[3]
        
        if os.path.exists(output_file):
            os.remove(output_file)

        with open(output_file, 'a') as out_f:
            for f in os.listdir(input_dir):
                input_file = os.path.join(input_dir, f)
                with open(input_file, 'r', encoding='utf-8') as in_f:
                    content = in_f.read()
                    out_f.write(content + "\n")

            


if __name__ == "__main__":
    main()