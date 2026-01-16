import sys
import os

def help():
    print("Usage: python analysis.py <command>")
    print("List of commands:")
    print("  ")


def process_tagged_file(file_path):
    """
    Process a tagged file and count trigram occurrences.
    
    Args:
        file_path: Path to the tagged file
    Returns:
        Dictionary with trigrams as keys and counts as values
    """
    trigram_count = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                 
                tags = [token.split('/')[1] for token in line.strip().split()]
                for i in range(len(tags) - 2):
                    trigram = (tags[i], tags[i + 1], tags[i + 2])
                    trigram_count[trigram] = trigram_count.get(trigram, 0) + 1

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {}
    
    return trigram_count

def write_trigrams(file_path, trigrams, threshold=0):
    with open(file_path, 'w', encoding='utf-8') as out_f:
        for trigram, count in sorted(trigrams.items()):
            if count >= threshold:
                out_f.write(f"{trigram}\t{count}\n")

def read_trigrams(file_path):
    """
    Read a trigram file and return a trigram count dictionary.
    
    Args:
        file_path: Path to the trigram file
    Returns:
        Dictionary with trigrams as keys and counts as values
    """
    trigram_count = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                trigram_str, count = parts
                trigram = tuple(trigram_str.strip("()").replace("'", "").split(", "))
                trigram_count[trigram] = int(count)
    return trigram_count

def query_tag_trigrams(trigrams, query, threshold=0, skip_unknown=False):
    """
    Query trigrams based on a tag pattern.
    
    Args:
        trigrams: Dictionary with trigrams as keys and counts as values
        query: Tuple with three elements representing the tag pattern (use '*' as wildcard)
        
    Returns:
        List of matching trigrams with their counts
    """
    results = []
    for trigram, count in trigrams.items():
        if count < threshold:
            continue
        if skip_unknown and 'UNK' in trigram:
            continue
        if (trigram[0] == query[0] or query[0] == "*") and \
           (trigram[1] == query[1] or query[1] == "*") and \
           (trigram[2] == query[2] or query[2] == "*"):
            results.append((trigram, count))
    return results

def find_words_from_pattern(tagged_file_path, start_tag, end_tag):
    """
    Find words matching a given tag pattern from trigrams.
    
    Args:
        tagged_file_path: Path to the tagged file
        start_tag: The starting tag
        end_tag: The ending tag 
        
    Returns:
        List of matching words with their counts
    """

    word_count = {}
    # Logic to find words based on the query pattern would go here.
    try:
        with open(tagged_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                 
                tags = [token.split('/') for token in line.strip().split()]
                for i in range(len(tags) - 2):
                    if (tags[i][1] == start_tag) and \
                       (tags[i + 1][1] == "UNK") and \
                       (tags[i + 2][1] == end_tag):
                        word = tags[i + 1][0]
                        word_count[word] = word_count.get(word, 0) + 1
                        

    except Exception as e:
        print(f"Error processing file {tagged_file_path}: {e}")
        return {}
    return word_count

def find_relations_from_pattern(tagged_file_path, pattern):
    """
    Find relations matching a given tag pattern from trigrams.
    
    Args:
        tagged_file_path: Path to the tagged file
        
    Returns:
        List of matching relations with their counts
    """

    relation_count = {}
    print("-->")
    # Logic to find relations based on the query pattern would go here.
    try:
        with open(tagged_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                
                tags = [token.split('/') for token in line.strip().split()]
                for i in range(len(tags) - 2):
                    if (tags[i][1] == pattern[0]) and \
                       (tags[i + 1][1] == pattern[1]) and \
                       (tags[i + 2][1] == pattern[2]):
                        relation = (tags[i][0], tags[i + 2][0])
                        relation_count[relation] = relation_count.get(relation, 0) + 1

    except Exception as e:
        print(f"Error processing file {tagged_file_path}: {e}")
        return {}
    return relation_count

def main():

    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: python trigrams.py create <input_file> <output_file> threshold")
            sys.exit(1)

        input_file = sys.argv[2]
        output_file = sys.argv[3]

        trigrams = process_tagged_file(input_file)
        try:
            write_trigrams(output_file, trigrams)
        except Exception as e:
            print(f"Error writing trigrams to file {output_file}: {e}")

    elif command == "create-batch":
        if len(sys.argv) != 4:
            print("Usage: python trigrams.py create-batch <input_directory> <output_directory>")
            sys.exit(1)

        input_directory = sys.argv[2]
        output_directory = sys.argv[3]

        if not os.path.isdir(input_directory):
            print("Error. Provided input directory does not exist. Exiting.")
            sys.exit(1)

        if not os.path.isdir(output_directory):
            print("Error. Provided output directory does not exist. Exiting.")
            sys.exit(1)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for filename in os.listdir(input_directory):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(filename))[0]}.tritags")

            print(f"Processing file: {input_path}")
            trigrams = process_tagged_file(input_path)
            try:
                write_trigrams(output_path, trigrams)
                print(f"Trigrams written to: {output_path}")
            except Exception as e:
                print(f"Error writing trigrams to file {output_path}: {e}")

    elif command == "merge-batch":
        if len(sys.argv) != 4:
            print("Usage: python trigrams.py merge-batch <input_directory> <output_file>")
            sys.exit(1)

        input_directory = sys.argv[2]
        output_file = sys.argv[3]

        merged_trigrams = {}

        for filename in os.listdir(input_directory):
            input_path = os.path.join(input_directory, filename)
            try:
                print(f"Merging trigrams from file: {input_path}")
                trigrams = read_trigrams(input_path)
                for trigram, count in trigrams.items():
                    merged_trigrams[trigram] = merged_trigrams.get(trigram, 0) + count
            except Exception as e:
                print(f"Error reading trigrams from file {input_path}: {e}")

        try:
            write_trigrams(output_file, merged_trigrams)
            print(f"Merged trigrams written to: {output_file}")
        except Exception as e:
            print(f"Error writing merged trigrams to file {output_file}: {e}")

    elif command == "query-tag-trigrams":
        if len(sys.argv) < 8:
            print("Usage: python trigrams.py query-tag-trigrams <input_file> <output_file> <target_tag> <threshold1> <threshold2> <threshold3> <support>")
            sys.exit(1)

        input_file = sys.argv[2]
        output_file = sys.argv[3]

        trigrams = read_trigrams(input_file)
        target_tag1 = sys.argv[4]
        target_tag2 = sys.argv[5]
        target_tag3 = sys.argv[6]
        threshold1 = int(sys.argv[7])

        results = query_tag_trigrams(trigrams, (target_tag1, target_tag2, target_tag3), threshold=threshold1)
        for trigram, count in results:
            print(trigram, " --> total:", count)


    elif command == "query-target-trigrams":
        if len(sys.argv) < 8:
            print("Usage: python trigrams.py query-tag-trigrams <input_file> <output_file> <target_tag> <threshold1> <threshold2> <threshold3> <support>")
            sys.exit(1)

        input_file = sys.argv[2]
        output_file = sys.argv[3]

        trigrams = read_trigrams(input_file)
        #target_tag = 'AJNS'
        #target_tag = 'NMS'
        #target_tag = 'NFS'
        target_tag1 = sys.argv[4]
        threshold1 = int(sys.argv[5])
        threshold2 = int(sys.argv[6])
        threshold3 = int(sys.argv[7])

        candidates = query_tag_trigrams(trigrams, ('*',target_tag,'*'), threshold=threshold1, skip_unknown=True)
        for trigram, count in candidates:
            #print(f"'{trigram}'\t{count}")
            candidate = (trigram[0], "*", trigram[2])
            result = query_tag_trigrams(trigrams, candidate, threshold=threshold2, skip_unknown=False)

            #total = 0
            #for t, c in result:
            #    total += c

            if len(result) < threshold3:
                print(candidate, " --> total:", count)
                for t, c in result:
                    print(f"    '{t}'\t{c}")

    elif command == "search-words-by-pattern":
        if len(sys.argv) < 6:
            print("Usage: python trigrams.py search-words-by-pattern <input_file> <tag1> <tag2> <tag3> threshold")
            sys.exit(1)

        input_file = sys.argv[2]

        #pattern = ["LAS", "DE"]
        #pattern = ["LOS", "DE"]
        #pattern = ["LA", "NFS"]
        tag1 = sys.argv[3]
        tag3 = sys.argv[4]
        threshold = int(sys.argv[5])
        result = find_words_from_pattern(input_file, tag1, tag3)
        for word, count in result.items():
            if count >= threshold:
                print(f"{word}")

    elif command == "search-realtions-by-pattern":
        if len(sys.argv) < 2:
            print("Usage: python trigrams.py search-realtions-by-pattern <input_file> <tag1> <tag2> <tag3> threshold")
            sys.exit(1)

        input_file = sys.argv[2]

        nouns = ["NMS", "NFS", "NMP", "NFP"]
        for n in nouns:
            for m in nouns:
                pattern = [n, "DE", m]
                print(f"Searching pattern: {pattern}")
                result = find_relations_from_pattern(input_file, pattern)
                for word, count in result.items():
                    print(f"{word}\t{count}")
        pattern = ["NMS", "DE", "NMS"]
        """
        #threshold = int(sys.argv[4])
        result = find_relations_from_pattern(input_file, pattern)
        for word, count in result.items():
            #if count >= threshold:
            print(f"{word}")
        """
if __name__ == "__main__":
    main()