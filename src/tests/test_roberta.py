import os
from src.models.ModelManager import ModelManager


def generic_test_for_hf(in_test, dataset_type):
	from src.models.huggingface.roberta import (
		HuggingFaceModel
	)
	mdl = HuggingFaceModel()
	mm = ModelManager(mdl, dataset_type=dataset_type, flat_y=True)
	mm.predict(in_test)
	mm.test(in_test)


def test_allocine_hugging_face():
	if "CI" in os.environ.keys():
		return True
		generic_test_for_hf('src/tests/dataset_allocine_100.csv', "tri")


def test_zemmour_hugging_face():
	if "CI" in os.environ.keys():
		return True
		generic_test_for_hf(
			'src/tests/Zemmour_135_tweets_labelled.csv', "tri")


def test_alexset_hugging_face():
	if "CI" in os.environ.keys():
		return True
		generic_test_for_hf(
			'src/tests/test_set_240tweets_labeled_0410.csv', "bi")
