# Text_Analyser

## Introduction
...


## Running the app

## Requirements

1. Install [Python 3]
2. Install [pip]

### Commands
```sh
pip install -U pip setuptools wheel
pip install -U spacy

pip install --user -U nltk
pip install --user -U numpy

pip install -r requirements.txt

python -m spacy download fr_core_news_sm
python -m spacy download en_core_news_sm

python
import nltk
nltk.download('punct')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
CTRL-D

```

```sh
python3 app.js
```

[pip]: <https://pip.pypa.io/en/stable/installing/>
[Python 3]: <https://www.python.org/downloads/>
