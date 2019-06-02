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

- Run language2Selenium. If use StanfordcoreNLP instead of NLTK, please install stanfordcorenlp and download the model and set --use_corenlp as True. If you want to run selenium code, set --run_selenium as True.

  ```
  python language_parser.py [--run_selenium={True,False}] \
                            [--use_corenlp={True,False}]
  ```

## Examples



- Transform the language into Selenium code procedure

  ```
  # Raw input: Enter the "KAIST" in "SearchBox" and click the "Search" button.
  # NameTuple: [("SearchBox", 'q'), ("Search", 'btnK')]
  
  STEP0: Raw input
  Enter the "KAIST" in "SearchBox" and click the "Search" button
  
  STEP1: split language into clauses.
  ['enter the "KAIST" in "SearchBox" .', 'click the "Search" button .']
  
  STEP2: Assign the selenium function type for each of clauses.
  0:enter the "KAIST" in "SearchBox" . => write
  1:click the "Search" button . => click
  
  STEP3: Find argument for each function.
  {'ARG1': 'the " KAIST "', 'ARGM-LOC': 'in " SearchBox "', 'V': 'enter'}
  ------------------------------
  Raw Input: enter the "KAIST" in "SearchBox" .
  Function Type and word: write  enter
  Target Name: in " SearchBox "
  Argument Names: ['the " KAIST "']
  ------------------------------
  {'ARG1': 'the " Search " button', 'V': 'click'}
  ------------------------------
  Raw Input: click the "Search" button .
  Function Type and word: click  click
  Target Name: the " Search " button
  ------------------------------
  
  STEP4: Make Selenium code with name-tuple.
  
  STEP5: Run code! (Optional)
  
  STEP6: Make python code
  output file name: ./output/testfile_0.py
  
  
  output code: 
  from selenium import webdriver
  
  Input = 'Enter the "KAIST" in "SearchBox" and click the "Search" button'
  
  driver_path = "./../dat/chromedriver.exe"
  driver = webdriver.Chrome(driver_path)
  driver.implicitly_wait(3)
  driver.get('https://google.com')
  
  # enter the "KAIST" in "SearchBox" .
  driver.find_element_by_name('q').send_keys('KAIST')
  
  # click the "Search" button .
  driver.find_element_by_name("btnK").click()
  ```