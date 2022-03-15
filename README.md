# SentimentalBB

En 2021 la France a été classée comme démocratie défaillante par le [Democracy Index](https://en.wikipedia.org/wiki/Democracy_Index#:~:text=The%20Democracy%20Index%20is%20an,the%20weekly%20newspaper%20The%20Economist.).

Nos démocraties se numérisent depuis plusieurs années, et une part croissante du débat public se joue dorénavant sur les réseaux sociaux. 
Alors qu’en période d'élections les [débats télévisées sont encadrées par l’ARCOM](https://www.arcom.fr/presse/larcom-le-regulateur-de-la-communication-audiovisuelle-et-numerique-dossier-de-presse) (ex-CSA), les débats au sein des réseaux sociaux échappent encore à un contrôle clair, et notamment par manque de métriques caractérisant les enjeux qui les traversent.

En tant que citoyens, et en tant qu'étudiants dans l’intelligence artificielle nous ressentons le besoin de mettre au service de notre démocratie des outils permettant de décrypter une partie du débat politique qui se déroule aujourd’hui sur Twitter.

A cet effet, nous étudions aujourd’hui le sentiment de la twittosphère à l’encontre des différents candidats en fonction du temps.

Merci de l’attention que vous portez à notre travail, tout commentaire et toute aide est la bienvenue.

==============================

# How to run as a module

```sh
poetry run python -m src --argument
```

## How to download the datasets:

### AclIMDB

```python
poetry run python -m src data --download aclImdb
```


### Twitter
One can download tweets from twitter, a candidat must be mention:

```python
poetry run python -m src data --download twitter --mention [candidat]
```
[candidat] must be within ["Pecresse", "Zemmour", "Dupont-Aignan", "Melenchon", "Le Pen", "Lassalle", "Hidalgo", "Macron", "Jadot", "Roussel", "Arthaud", "Poutou"]

You have several more parameters accessible:
* `--text`: text you wish to find in the tweet: `--text retraite`
* `--start_time`: date from which you want to start to collect the tweets (need to follow the format: `YYYY-mm-DD HH:MM`, `HH` and `MM` are optional)
* `--end_time`: date until which you want to collect the tweets (need to follow the format: `YYYY-mm-DD HH:MM`, `HH` and `MM` are optional)

The dataset collected from twitter are saved into file: `data/raw/[candidat]/twitter_{mention}_{start_time}_{end_time}.csv`

# How to launch fast api

```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```

Then visits: <http://localhost:8000/docs>

# With the docker

```sh
docker build -t inference:latest .

docker run -p 8000:8000 --name inference_container inference:latest
```

# With Docker Compose

```
docker-compose up
```

# Project architecture

Template for all the future project of the Laboratory of 42-AI

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

# Contributors

* [Matthieu David](https://github.com/madvid) - mdavid@student.42.fr
* [Alexandre Gilmet](https://github.com/goldimet) - agilmet@student.42.fr
* [Guillaume Sallé](https://github.com/guillaume-salle) - gusalle@student.42.fr
* [Archibald Thirion](https://github.com/archips) - athirion@student.42.fr
* [Clément Vidon](https://github.com/clemedon) - cvidon@student.42.fr
