# Friday

<img src="https://github.com/bowbowbow/Friday/blob/master/browser_extension/chrome/assets/img/icon-128.png" width="128">

Friday is a Chrome extension that automatically transforms test scenarios written in natural language into selenium code.

This is the project implementation of team 5 for KAIST, CS453 Automated Software Testing, Spring 2019.

## Installation

This project is being developed in Python 3.6.

1. Install the required dependencies.

   ```
   pip install numpy torch allennlp nltk stanfordcorenlp stanfordcorenlp
   ```
   
2. Download [glove](https://nlp.stanford.edu/projects/glove/).

   ```bash
   mkdir dat
   cd dat
   wget http://nlp.stanford.edu/data/glove.6B.zip
   unzip glove.6B.zip
   ```
   
3. [Download chromedriver](http://chromedriver.chromium.org/downloads) with your Chrome version and locate into `/dat` directory. 
    
4. (Optional) Download stanfordcorenlp model.

    ```bash
    cd dat
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
    unzip stanford-corenlp-full-2018-10-05.zip
    ```

## Getting Started

```bash
python language_parser.py
```

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

## Run detail

- Run language2Selenium. If use StanfordcoreNLP instead of NLTK, please install stanfordcorenlp and download the model and set --use_corenlp as True. If you want to run selenium code, set --run_selenium as True. By default, both --run_selenium and --use_corenlp is False.

  ```bash
  python language_parser.py [--run_selenium={True,False}] \
                            [--use_corenlp={True,False}]
                            
  # Example
  python language_parser.py --use_corenlp            
  ```

### Examples

- Transform the language into Selenium code procedure

  ```
  Raw input: : "Open the \"https://google.com\" and Enter the \"Iron man\" in #1 and click the #2.\nWait the \"3 seconds\" and Check if \"Robert Downey\" is on the page"
  
  "selectors": [
    {
      "path": ".gLFyf",
      "location": "https://www.google.com/",
      "tagId": 1
    },
    {
      "path": "center:nth-child(1) > .gNO89b",
      "location": "https://www.google.com/",
      "tagId": 2
    }]

  
  STEP0: Raw input
  Open the "https://google.com" and Enter the "Iron man" in #1 and click the #2.
  Wait the "3 seconds" and Check if "Robert Downey" is on the page

  STEP1: split language into clauses.
  ['open the "https://google.com" .', 'enter the "Iron man" in #1 .', 'click the #2 .', 'wait the "3 seconds" .', 'check if "Robert Downey" is on the page .']

  STEP2: Assign the selenium function type for each of clauses.
  0:open the "https://google.com" . => move_url
  1:enter the "Iron man" in #1 . => write
  2:click the #2 . => click
  3:wait the "3 seconds" . => wait
  4:check if "Robert Downey" is on the page . => contain_value

  STEP3: Find argument for each function.
  {'ARG1': 'the " https://google.com "', 'V': 'open'}
  ------------------------------
  Raw Input: open the "https://google.com" .
  Function Type and word: move_url  open
  Argument Names: ['the " https://google.com "']
  ------------------------------
  {'ARG0': 'the " Iron man "', 'ARGM-LOC': 'in # 1', 'V': 'enter'}
  ------------------------------
  Raw Input: enter the "Iron man" in #1 .
  Function Type and word: write  enter
  Target Name: in # 1
  Argument Names: ['the " Iron man "']
  ------------------------------
  {'ARG1': 'the # 2', 'V': 'click'}
  ------------------------------
  Raw Input: click the #2 .
  Function Type and word: click  click
  Target Name: the # 2
  ------------------------------
  {'ARGM-TMP': 'the " 3 seconds', 'V': 'wait'}
  ------------------------------
  Raw Input: wait the "3 seconds" .
  Function Type and word: wait  wait
  Argument Names: ['the " 3 seconds']
  ------------------------------
  {'ARG1': 'if " Robert Downey " is on the page', 'V': 'check'}
  ------------------------------
  Raw Input: check if "Robert Downey" is on the page .
  Function Type and word: contain_value  check
  Argument Names: ['if " Robert Downey " is on the page']
  ------------------------------

  STEP4: Make Selenium code with name-tuple.

  STEP5: Run code! (Optional)

  STEP6: Make python code
  output file name: ./output/testfile_0.py
  
  
  output code: 
  from selenium import webdriver

  Input = 'Open the "https://google.com" and Enter the "Iron man" in #1 and click the #2. Wait the "3 seconds" and Check if "Robert Downey" is on the page'

  driver_path = "./../dat/chromedriver.exe"
  driver = webdriver.Chrome(driver_path)
  driver.implicitly_wait(1)

  # open the "https://google.com" .
  driver.get('https://google.com')

  # enter the "Iron man" in #1 .
  driver.find_element_by_css_selector('.gLFyf').send_keys('Iron man')

  # click the #2 .
  driver.find_element_by_css_selector("center:nth-child(1) > .gNO89b").click()

  # wait the "3 seconds" .
  import time
  time.sleep(3)

  # check if "Robert Downey" is on the page .
  assert "Robert Downey" in driver.page_source  
  ```
