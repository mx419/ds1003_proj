## User Guide
- DS-GA-1003  Final Project: Legal Outcome Prediction
- Advisor: Dr.Daniel Chen
- Team Member:
  - Muhe Xie(mx419) mx419@nyu.edu
  - Sida Ye(sy1743) sy1743@nyu.edu
  - Xingye Zhang(xz601) xz601@nyu.edu

### Part 1: Environment Setup
1. run the following commands to download our projects
``` sh
$ git clone [git-repo-url]
```
2. Make sure you have installed sklearn, numpy and pandas packages.

### Part 2 : Label generation

Run the following command in terminal. It will generate new files with binary panel vote label.
``` sh
$ python label_generation.py
```
Combine all legal fields csv into one
``` sh
$ awk 'FNR > 1' ./data/modified_case/*.csv > ./data/bigfile.csv
```

### Part 3: Data Clean, Merge and Feature Selection

1. Clean Vocab_map_text file.
2. Data Merge and feature selection. It will generate 16 files in different legal fields. 

3. Recommendation and predication
    * Get information of usage of the station on that particular date on historical date and get recommendation on the station.
    * Get two alternative stations nearby which meet with the criterion: I. within 15-minute walk, II. predicted to be recommended.

### Part 4 : Modeling and Generating key word features

1. Find target word feature id
``` sh
python word_generate.py
```
It will save a pickle file, which contains the target word id list we need to find in Vocab_map_text file.

2. Match targe word feature id with its real ngram

3. Run the following command, which will generate the AUC performance for each legal field and positive, negative word list in terminal.
``` sh
python modeling.py
```
If you want to save the result, you can run
``` sh
python modeling.py > result.txt
```


### Part 4: How to run the program

In terminal, enter the command to run the program:

``` sh
$ cd sy1743
$ python main.py
```




### Acknowledgement
- Law Data resource from Daniel Chen
