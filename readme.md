# Creating a Python Virtual Environment

## Using venv (Python 3.3+)

```bash
python3 -m venv .venv
pip install scipy
pip install scikit-learn
```


## Activate the virtual environment

**Linux/macOS:**
```bash
. .venv/bin/activate
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

## Deactivate
```bash
deactivate
```

# Commands

##  Unigrams

### File to unigrams
Single file text to unigrams
python unigrams.py create <input raw text file> <output file name>

Ex.:
python src/unigrams.py create data/raw/gutenberg/granos_de_oro.txt output/unigrams/gutenberg/granos_de_oro.unigrams 0

### Batch of files to unigrams
python src/unigrams.py create-batch data/raw/gutenberg output/unigrams/gutenberg 0


### Merge unigrams
python src/unigrams.py merge-batch output/unigrams/gutenberg output/merged/gutenberg.unigrams 0

### Compare

python src/unigrams.py compare data/test/dict1.unigrams data/test/dict2.unigrams 

python src/unigrams.py compare output/unigrams/gutenberg/azul.unigrams output/unigrams/gutenberg/niebla.unigrams 


### Analysis

Filter unigrams:
Ex.:

python src/unigrams.py filter output/merged/gutenberg.unigrams 200

python src/unigrams.py filter output/dict/gutenberg_granos_de_oro.dict 40

## Bigrams

### File to bigrams
Ex.:
python src/bigrams.py create data/raw/gutenberg_granos_de_oro.txt output/bigrams/gutenberg_granos_de_oro.bigrams

### Batch of files to bigrams
python src/bigrams.py create-batch data/raw/gutenberg output/bigrams/gutenberg 0

### Merge bigrams
python src/bigrams.py merge-batch output/bigrams/gutenberg output/merged/gutenberg.bigrams 0




## ML Train:

### Noun finder

#### Train model:
python -m ml.nounfinder train ../output/merged/gutenberg.bigrams ../data/tagged/nouns_vs_other.dtag ../models/nounfinder.pkl

#### Predict
python -m ml.nounfinder predict  ../models/nounfinder.pkl ../output/merged/gutenberg.bigrams ../output/merged/gutenberg.unigrams 600

Tagged corpus:

python src/preprocess.py preprocess ./data/raw/gutenberg_granos_de_oro.txt output/preprocess/gutenberg_granos_de_oro.txt



## Preprocess

### Single text file
python src/preprocess.py preprocess ./data/raw/gutenberg/granos_de_oro.txt output/preprocess/granos_de_oro.txt

### Batch text files
python src/preprocess.py preprocess-batch ./data/raw/gutenberg output/preprocess/gutenberg


## Tagged corpus

python src/tagger.py tag ./data/tagged/nouns.dtag ./output/preprocess/granos_de_oro.txt ./output/tagged/granos_de_oro.tagged

python src/tagger.py tag-batch ./data/tagged/nouns.dtag ./output/preprocess/guttenberg ./output/tagged/guttenberg

python src/tagger.py merge ./output/tagged/guttenberg ./output/merged/gutenberg.tagged

## Tag trigrams

python src/trigrams.py create ./output/tagged/granos_de_oro.txt ./output/tritags/granos_de_oro.tritags

python src/trigrams.py create-batch ./output/tagged/guttenberg ./output/tritags/guttenberg

python src/trigrams.py merge-batch ./output/tritags/guttenberg ./output/merged/gutenberg.tritags



python src/trigrams.py query ./output/merged/gutenberg.tritags ./output/test

python src/trigrams.py search ./output/merged/gutenberg.tagged



python src/tagger.py merge ./output/tagged ./output/merged/gutenberg.tagged



python src/tagger.py tag-batch ./data/tagged/pos.dtag ./output/preprocess ./output/tagged
python src/tagger.py merge ./output/tagged ./output/merged/gutenberg.tagged
python src/trigrams.py create-batch ./output/tagged ./output/tritags
python src/trigrams.py merge-batch ./output/tritags ./output/merged/gutenberg.tritags


# 
threshold1: number of min to consider   * TGT * -> [r1, r2, ..., rn], utterances(ri) >= threshold1 
threshold2: rule search
threshold3: number of tags within the rule


python src/trigrams.py query-tag-trigrams ./output/merged/gutenberg.tritags ./output/test NFS 0 
python src/trigrams.py search-words-by-pattern ./output/merged/gutenberg.tagged LA NFS 10
python src/trigrams.py search-realtions-by-pattern ./output/merged/gutenberg.tagged