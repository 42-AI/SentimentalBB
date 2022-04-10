### Metadata test_set_240tweets_0410.csv

**Timestamp:** csv labelised on 2022-04-10 at 1pm

**Done by:** Alexandre

**Original dataset:** 20 tweets for each candidate from one  file for each candidate. File has been randomly selected from all the predict files for the candidate

**Labels:** Positive(1,0)/Negative(0,1)/Neutral(0,0)

**Dataset Remarks**:
+ lots of tweets with many candidates mentioned in the tweet
+ Some tweets with not much more than a web link or image
+ Some tweets are discussions between 2 twitter users and the topic of the tweet is related to their discussion, not the candidate

**Labeling Method**:
+ The analysis of the sentiment has been **done only on interpreting whether or not the text is somtehing positive or negative  in general**, not in context nor related to the candidate.
  + Exple1: "@Zemmour Trop d'insécurité en France!" ==> negative
  + Exple2: "@Lasalle Mais laissez-le parler! On ne lui donne pas assez de temps de parole" ==> negative
  + Exple3 for Melenchon: "@Zemmour @Lepen Tous ces fachos faut les éliminer @Melenchon" ==> negative
  + Exple4: "@Zemmour @cnews @mamere @monpote Oui" ==> positive
+ **Irony** has been taken into account.
  + Exple: "@Macron Mais bein sur... Toujours plus de riches! Bravo!" ==> negative.
+ **Neutral** has been used when no info in the tweet (link, only emoji,...) or on factual text
  + Exple1: "@Zemmour angry emoji" ==> neutral
  + Exple2: "@Zemmour RDV à l'arena de Metz pour un nouveau meeting!" ==> Neutral