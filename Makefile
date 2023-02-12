.PHONY: install get-corpus train-eng-cat

install:
	cd install-scripts && ./install.sh

get-corpus:
	cd languages && ./get-corpuses.sh
	
train-eng-cat:
	cd languages/eng-cat/ && ./voc.sh &&./train.sh

