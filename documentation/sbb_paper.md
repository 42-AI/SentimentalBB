- Title
    Sentimental Big Bro
- Introduction
 - Here you will speak about the general context in which your work has been done
    Les élections présidentielles ayant lieues dans les mois à venir nous avons
    décidé de créer un indicateur de popularité de chaque candidat en nous
    basant sur les données de Twitter.

    With the presidential elections coming up in the next few months, we
    decided to create a popularity indicator for each candidate based on
    Twitter data.
 - Why is your work needed and novel?
    Notre travail met en avant le pouvoir de l'IA pour avoir un aperçu au jour
    le jour de la température concernant les candidats aux présidentielles.

    Our work highlights the power of AI to provide a day-by-day snapshot of the
    temperature regarding presidential candidates.
 - One sentence to hype your reader
    Pour ce faire nous avons décidé d'avoir recours au [Natural Language
    Processing](https://www.NLP_DEF.com/), la branche de l'IA nous permettant
    de faire de l'analyse de sentiment.

    To do this we decided to use [Natural Language
    Processing](https://www.NLP_DEF.com/), the branch of AI that allows us to
    do sentiment analysis.
- Previous Work
 - Here is the good place to briefly cite/explain the things you used but which
   you did not construct. ie: your models
    Nous avons pris comme point de départ un BERT-like modèle pré-entrainé en
    français, à savoir [roBERTa](https://huggingface.co/roberta-base).

    We took as a starting point a BERT-like model pre-trained in French, namely
    [roBERTa](https://huggingface.co/roberta-base).
- Material and Methods
 - Data
   - Which data did you train on, and why?
    Nous nous sommes entrainés sur le dataset d'Allociné spécialement crée pour
    l'analyse de sentiment. Il est constitué de critiques de films en français
    et des labels 'positif' 'neutre' ou 'négatif'.

    We trained on the dataset of Allociné specially created for the sentiment
    analysis. It is made up of film reviews in French and the labels
    'positive', 'neutral' or 'negative'.
   - Which data did you predict on, and why?
    La données utilisées sont constituées de tweets récupérés via
    l’[API](http://www.API_DEF.com) Twitter. Nous collectons les tweets
    français qui mentionnent directement les candidats qui nous intéressent.

    The data used are tweets collected via the Twitter
    [API](http://www.API_DEF.com). We collected the French tweets that directly
    mention the candidates we are interested in.
 - Models
   - Which models did you try, and why?
    Nous avons testé deux modèles en commençant par [Naive
    Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html) pour avoir
    une première base et un [pipeline](http://www.PIPELINE_DEF.com) complet.
    Nous nous sommes ensuite concentré sur le modèle roBERTa pour affiner nos
    résultats.

    We tested two models starting with [Naive
    Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html) to have a
    first base and a complete [pipeline](http://www.PIPELINE_DEF.com).  We then
    focused on the roBERTa model to refine our results.
   - What were the results?
    VOIR AVEC GUILLAUME (PEUT ÊTRE ALEX?) POUR LES STATS FINALS
 - Visuals
   - What information did you try to express, and why your choice of figure is appropriate?
    On a choisi de représenter nos résultats sous forme d'un graphe à
    bâtonnets par candidat en fonction du temps.  On y retrouve les dates
    (mois jours) en abscisse et la proportion de positivité et de
    négativité du sentiment global en ordonnée.
    Ces visuels sont largement perfectibles et nous ont avant tout
    permit de valider le bon fonctionnement de notre pipeline.
    Ils ont été généré quotidiennement et publié sur le site du projet
    et le Slack de l'asso 42AI pendant la semaine précédent le
    résultat des élections.

    We chose to represent our results as a bar graph per candidate
    versus time.  It shows the dates (months days) on the x-axis and
    the proportion of positivity and negativity of the overall feeling
    on the y-axis.
    These visuals are largely perfectible and have primarily permitted
    us to validate the proper functioning of our pipeline.
    They were generated daily and published on the project website and
    the Slack of the 42AI association during the week before the
    election result.
- Results
 - How confident are you in your model and why?
    La précision actuelle de notre modèle est de ??? et la corrélation avec les
    sondages officielles est positive mais le développement du projet a mis en
    lumière de nombreux biais qui nous mènent à penser que nos prédictions sont
    largement perfectibles.

    The current accuracy of our model is ??? and the correlation with official
    surveys is positive, but the development of the project has brought to
    light many biases that lead us to believe that our predictions are largely
    perfectible.
- Conclusion
 - What conclusion can we have from all your work?
    L'utilisation de Twitter pour faire de l'analyse de sentiment semble
    pertinente mais présente de nombreuses difficultés à commencer par les
    biais.

    Using Twitter for sentiment analysis seems relevant but presents many
    difficulties starting with bias.
- Discussion
 - If you had more time or more resources, what will you do?
    Avec plus de temps nous pourrions améliorer le modèle que nous utilisons et
    le spécialiser pour les Twits (problème des retweet, analyse des
    commentaires des Twits etc.) et particulièrement les Twits concernant la
    politique. Nous pourrions effectuer des labélisations manuelle, nous
    pencher sur les biais pour en éliminer un maximum.  Nous pourrions aussi
    utiliser d'autres métadonnées tels que la localisation géographique de
    chaque Twits et produire des visuels plus originaux.

    With more time we could improve the model we use and specialize it for
    tweets (retweet problem, analysis of comments of tweets etc.) and
    especially tweets about politics. We could do manual labeling, look at
    biases to eliminate as many as possible.  We could also use other metadata
    such as the geographical location of each Twit and produce more original
    visuals.
 - If you could see flourish new work after yours, what would you want it to be about?

