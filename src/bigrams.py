import sys
import os
import numpy as np
import json
import re

from preprocess import stopwords

def help():
    print("Usage: python analysis.py <command>")
    print("List of commands:")
    print("  ")

def read_bigrams(file_path):
    bigrams = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    bigram_str, count = parts
                    #print(bigram_str, count)
                    bigram = tuple(json.loads(bigram_str))
                    bigrams[bigram] = int(count)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return bigrams

def count_bigrams(file_path):
    bigrams = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                sentences = re.sub(r'[^a-zA-Záéíóúüñ ]', '\n', line.lower()).split('\n')
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    words = sentence.split()
                    for i in range(len(words) - 1):
                        bigram = (words[i].lower(), words[i + 1].lower())
                        bigrams[bigram] = bigrams.get(bigram, 0) + 1
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return bigrams

def write_bigrams(file_path, bigrams, threshold=0):
    with open(file_path, 'w', encoding='utf-8') as out_f:
        for bigram, count in sorted(bigrams.items()):
            if count >= threshold:
                json.dump(list(bigram), out_f, ensure_ascii=False)
                out_f.write(f"\t{count}\n")

def print_bigrams_filtered(bigrams, threshold):
    for bigram, count in bigrams.items():
        if count >= threshold:
            print(f"'{bigram}'\t{count}")

def query_bigrams(bigrams, query, threshold):
    for bigram, count in bigrams.items():
        if (bigram[0] == query[0] or query[0] == "*") and (bigram[1] == query[1] or query[1] == "*"):
            if count >= threshold:
                print(f"'{bigram}'\t{count}")

def make_noun_ft_array(target, bigrams):
    result = []
    tsum = 0
    for stopword in stopwords:    
        try:
            temp = bigrams[(stopword, target)]
            tsum = tsum + temp
            result.append(temp)
        except KeyError:
             result.append(0)
    if tsum == 0:
        return np.array(result)
    return np.array(result)/tsum

def read_tagged(file_path):
    result = {}
    current = []
    current_class = None
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith("#"):
                if len(current) > 0 and current_class is not None:
                    result[current_class] = current
                    current = []
                current_class = line.strip()[1:].strip()
            else:
                current.append(line.strip())
    
    if len(current) > 0 and current_class is not None:
        result[current_class] = current

    return result


def main():

    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 5:
            print("Usage: python bigrams.py create <input_file> <output_file> threshold")
            sys.exit(1)

        input_file = sys.argv[2]
        output_file = sys.argv[3]
        threshold = int(sys.argv[4])

        bigrams = count_bigrams(input_file)
        write_bigrams(output_file, bigrams, threshold)


        #print_bigrams_filtered(bigrams, threshold=20)
        #query_bigrams(bigrams, ("un", "*"), threshold=5)
        
        #'hombre', 'hombres', 'mundo', 'pueblo', 'pueblos', 'tierra', 'vida'

        #keyword = sys.argv[3]
        #query_bigrams(bigrams, ("*", keyword), threshold=threshold)
        #query_bigrams(bigrams, (keyword, "*"), threshold=threshold)

    elif command == "create-batch":
        if len(sys.argv) < 5:
            print("Usage: python bigrams.py create-batch <input_file> <output_file> threshold")
            sys.exit(1)

        input_directory = sys.argv[2]
        output_directory = sys.argv[3]
        threshold = int(sys.argv[-1])

        for f in os.listdir(input_directory):
            input_file = os.path.join(input_directory, f)
            bigrams = None
            if os.path.isfile(input_file):
                print(f"Processing input file: {input_file}")
                bigrams = count_bigrams(input_file)

            if bigrams is not None:
                output_file = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_file))[0]}.bigrams")
                try:
                    write_bigrams(output_file, bigrams, threshold)

                    print(f"Input file: {input_file}")
                    print(f"Dictionary written: {output_file}")
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

        for f in os.listdir(input_directory):
            dict_file = os.path.join(input_directory, f)
            if os.path.isfile(dict_file):
                try:
                    dictionary = read_bigrams(dict_file)
                    for word, count in dictionary.items():
                        merged_dict[word] = merged_dict.get(word, 0) + int(count)
                except Exception as e:
                    print(f"Error reading dictionary file {dict_file}: {e}")

            try:
                write_bigrams(output_file, merged_dict, threshold)
                print(f"Merged dictionary {dict_file} written to {output_file}")
            except Exception as e:
                print(f"Error writing to output file {output_file}: {e}")

    else:
        print(f"Unknown command: {command}")
        help()
        sys.exit(1)

if __name__ == "__main__":
    main()