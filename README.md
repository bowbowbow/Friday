# Friday

This is the project implementation of team 5 for KAIST, CS453 Automated Software Testing, Spring 2019.



## Prerequisites

- python3.6
- numpy
- torch
- allennlp
- nltk
- (Optional: stanfordcorenlp)



- Download `glove.6B.200d.txt` from [here](http://nlp.stanford.edu/data/glove.6B.zip) and locate it into `/dat` directory.

- Download appropriate version of  `chromedriver.exe` with your Chrome version and locate into `/dat` directory.

- (Optional: Download stanfordcorenlp model from [here](http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip) and locate in project directory. If use NLTK, don't need to download this.)

  

## Package Structure

Below is the overview of directory structure.

```text
Friday/
├── browser_extension
│     └── TBD...
│     └── TBD...
│          └── TBD...
│
├── output
│     └── testfile_#.py
│
├── dat/
│     └── chromedriver.exe
│     └── glove.6B.200d.txt
│
├── func.py
├── language_parser.py  # language2selenium main function
├── utils.py
├── README.md
├── .gitignore
```



## Build

- Run language2Selenium. If use StanfordcoreNLP instead of NLTK, please install stanfordcorenlp and download the model and set --use_corenlp as True.

  ```
  python language_parser.py [--run_selenium={True,False}] \
                            [--use_corenlp={True,False}]
  ```

## Examples

TBD
