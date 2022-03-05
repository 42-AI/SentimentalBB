wget http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz

mkdir -p ./data/raw/StandfordSentiments

mv aclImdb_v1.tar.gz ./data/raw/StandfordSentiments

tar -zxvf ./data/raw/StandfordSentiments/aclImdb_v1.tar.gz -C ./data/raw/StandfordSentiments
