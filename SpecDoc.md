# Specification Document Sentimental BB

## A. WHAT THE PROGRAM DOES


### A1. DATA

The 1st subpart of the program is related to datasets in general.

#### A1a. Download/Scrap

**Goal**: Download or scrap data online to store them in data/raw.

**1) Use Case Allocine**:

The dataset Allocine must be downloaded via the CLI and saved in data/raw/allocine with the command below. This command normally needs to be executed once and the dataset created needs to pushed via dvc so that it can later be retrieved with `dvc pull`. 

+ Called via CLI
+ Command: `poetry run python -m src data --download allocine`
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: create csv in _data/raw/allocine/allocine\_raw.csv_ formatted as such <span style="color: red;">tbd</span>

The source code to perform this action must be written in _src/data/download/download\_allocine.py_

**2) Use Case Twitter**:

Every day, <span style="color: red;">X</span> tweets mentionning every candidate must be downloaded from twitter to _data/raw/twitter/candidate\_name_ with the command below. The tweets mentionning a candidate must be formatted as such <span style="color: red;">tbd</span> and named as such <span style="color: red;">tbd</span>.

+ Called via CLI
+ Command: `poetry run python -m src data --download twitter`
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: create csvs containing <span style="color: red;">nb</span> tweets for every candidate in _data/raw/twitter/candidate\_name_

The source code to perform this action must be written in _src/data/download/download\_twitter.py_


#### A1b. Make Dataset

**Goal**: From _data/raw_ or _data/processed_, Make a processessed csv dataset.  

**1) Use Case Allocine**:

There are 3 types of datasets that need to be made for allocine:

<span style="color: blue;">1. Train</span>

+ Creates a dataset on which the models will train.
+ Called via CLI
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: creates a csv named _allocine_nbofreviews\_reviews_totrain_ in _data/processed/train_ with thousands of reviews formatted as such:
  - 'text': contains the text review
  - 'Positive': contains 1 if review is positive, 0 otherwise
  - 'Negative': contains 1 if review is negative, 0 otherwise

The source code to perform this action must be written in a function in _src/data/make\_dataset/allocine.py_


<span style="color: blue;">2. Predict</span>

+ Creates a dataset on which the models will predict.
+ Called via CLI
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: creates a csv named _allocine_nbofreviews\_reviews_topredict_ in _data/processed/predict_ with thousands of reviews (!Warning: must be different reviews then the ones used to train) formatted as such:
  - 'text': contains the text review

The source code to perform this action must be written in a function in _src/data/make\_dataset/allocine.py_


<span style="color: blue;">3. Test</span>

+ Creates a dataset on which the models will be tested. Warning: Stored in _src/test_ as this small data needs to be git pushed for the unit tests.
+ Called via CLI
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: creates a csv named _allocine_nbofreviews\_reviews_totest_ in _src/test_ with hundreeds of reviews (!Warning: must be different reviews then the ones used to train) formatted as such:
  - 'text': contains the text review
  - 'Positive': contains 1 if review is positive, 0 otherwise
  - 'Negative': contains 1 if review is negative, 0 otherwise

The source code to perform this action must be written in a function in _src/data/make\_dataset/allocine.py


**2) Use Case Twitter**:

There are 4 types of datasets that need to be made for twitter:

<span style="color: blue;">1. Preprocessed Remove RTs</span>

+ From all the tweets in raw, creates csvs with all the tweets in raw without the Retweets.
+ Called via CLI
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: creates csvs with similar formats as the tweets in Raw <span style="color: red;">tbd</span> and store them in data/processed/prepro 

The source code to perform this action must be written in a function in _src/data/make\_dataset/twitter.py_

<span style="color: blue;">2. Predict</span>

+ From all the tweets in _data/processed/prepro_, creates a csv with all the tweets for a specific candidate and for a specific day. 
+ Called via CLI
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: creates csvs as _data/processed/predict/day/candidate\_name.csv_formatted as such:
  - 'candidate': name of candidate (see how to name candidates in \_\_main.py\_\_)
  - 'time': timestamp of tweet formatted as such <span style="color: red;">tbd</span>
  - 'text': text of tweet

The source code to perform this action must be written in a function in _src/data/make\_dataset/twitter.py_


<span style="color: blue;">3. Test</span>

+ From some tweets in _data/processed/prepro_ that MUST NOT be in _data/processed/predict_ (either removing them from predict or not including them in predict to begin with when doing make dataset twitter Predict), creates a non-labelled csv with hundreeds of tweets that will later be labelled in order to test a model.
+ The tweets must be selected randomly in terms of timestamp and have more or less the same nb of tweets for each candidate. 
+ Warning: Stored in _src/test_ as this small data needs to be git pushed for the unit tests.
+ Called via CLI
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: creates a csv as _src/test/nbtweets\_tweets\_date\_unlabelled.csv_ formatted as such:
  - 'candidate': name of candidate (see how to name candidates in \_\_main.py\_\_)
  - 'time': timestamp of tweet formatted as time in predict <span style="color: red;">tbd</span>
  - 'text': text of tweet
  - 'Positive': every value set to 0 as it yet has to be labelled
  - 'Negative': every value set to 0 as it yet has to be labelled

Once the csv is created, it will have to be manually labelled (via google sheet for exple) and the name of the csv will have to be updated to _nbtweets\_tweets\_date\_labelled.csv_

The source code to perform this action must be written in a function in _src/data/make\_dataset/twitter.py_

<span style="color: blue;">4. Train</span>

As of now, it appears that no twitter dataset will be used to train a model as it is recommanded to have at least thousands of labelled data to train a model and that the time needed to label all those tweets might be a waste of time.



#### A1c. Load Dataset

**Goal**: From csvs in _data/processed_, creates python objects such as np.array or pd.dataframes to be mostly used by functions and classes in models.

**Called**: as a library by other parts of the code

**1) Use Case Models**

<span style="color: red;">tbd</span>


The source code to perform these actions must be written in in _src/data/load\_dataset/.../.py_



### A2. FEATURES

The 2nd subpart of the program build features on top of the data python objects created by _load\_dataset_.

+ Used as a library by other parts of codes
+ Returns: Mainly returns python data objects with new features built on top

Not clear yet if we'll have to use it.

<span style="color: red;">tbd</span>


### A3. MODELS


The 3rd subpart of the program is related to everything related to model training/testing/predicting. In order to function it needs the appropriate dataset(s) made by data/make_dataset.

Before calling the parts here under in the CLI, it's good to know in advance if the needed code to make the needed dataset has already been done.


#### A3a. Train

**Goal**: Based on a chosen algo, chosen hyperparameters and chosen train data set stored in _data/processed/train_, train a model and outputs it in the folder _models_ in root. The ouput will mainly consists of weights  

+ Called via CLI <span style="color: red;">(but also as lib?)</span>
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: store weights in a folder in _models/_ <span style="color: red;">tbd</span>

The source code to perform this action must written in _src/models/typeoflibraryused/nameofalgo.py_


#### A3b. Test

**Goal**: Based on a chosen train model (weights), a chosen test set in _src/test_ and a chosen perofrmance metric, outputs the score of the model in a file <span style="color: red;">tbd</span> in _data/processed/results_ and outputs the csv used to test with the predictions added somewhere in _data/processed/results_ <span style="color: red;">tbd</span>. 

+ Called via CLI <span style="color: red;">(but also as lib?)</span> 
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: 
  - score of the model in a file <span style="color: red;">tbd</span> in _data/processed/results_
  - csv used to test with the predictions added 'Postivie_pred', 'Negative_pred' somewhere in _data/processed/results_ <span style="color: red;">tbd</span>

The source code to perform this action must written in _src/models/typeoflibraryused/nameofalgo.py_


#### A3c. Predict

**Goal**: Based on a chosen train model (weights), a chosen predict set in _data/processed/predict_ and a chosen perofrmance metric outputs the csv used to predict with the predictions added.

The source code to perform this action must written in _src/models/typeoflibraryused/nameofalgo.py_


**1) Use Case Allocine**:

<span style="color: red;">tbd</span>

**2) Use Case Twitter**:

Based on a csv from a specific candidate on a specific day in _data/processed/predict_, outputs the csv with the predictions.
<span style="color: red;">Possibility to do many candidates and many dates all at once?</span>

+ Called via CLI 
+ Command:  <span style="color: red;">tbd</span> 
+ Other Arguments:
  -  <span style="color: red;">tbd</span>
+ Outputs: csv as _data/processed/results/modelname\_timestampofcommand/day/candidate.csv formatted as such:
  - 'Candidate': candidate name
  - 'pred': 1 if positive, 0 if negative
  - 'datetime': same format as in prodict csv passed in input
  - 'text': text of tweet
  



### A4. TEST


The 4th part of the program is related to all the tests run in the CI/CD process.
For each new block of code, a corresponding unit test need to be added somewhere in _src/tests_ and the function written must start with "test_" to be tested by pytest.


### A5. VISUALIZATION


The 5th part of the program takes csv results and creates charts from it.

<span style="color: red;">tbd</span>


## B. DATA ARCHITECTURE

All the data are stored in the folder _data_ located in the root folder of the project. The data stored is not git push and in order to retrieve it, `dvc pull` must be done.

<span style="color: red;">tbd</span>