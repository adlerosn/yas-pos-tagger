all:
	make clean
	make create_dirs
	make split_train_test
	make train
	make tag
	make test_performance

split_train_test:
	python3 convert.py

train:
	python3 trainQuickStats.py
	python3 train.py

tag:
	python3 tag.py

test_performance:
	python3 joinTagAndText.py
	python3 prepareUnitexEvaluation3.py
	python3 prepareUnitexEvaluation4.py
	python3 runUnitexEvaluation.py

create_dirs:
	mkdir -p unitexable_test
	mkdir -p unitexable_train

clean:
	rm -rf unitexable_test
	rm -rf unitexable_train

pipdeps:
	sudo -H make pipdepswithsudo

pipdepswithsudo:
	python3 -m pip install -r requirements.txt

