all:
	virtualenv venv
	venv/bin/pip install -r requirements.txt
	venv/bin/python setup.py develop
	@echo "Voila, now you should be able to run "rslide" from the venv here"

upload:
	python setup.py sdist upload -r pypi

test_upload:
	python setup.py sdist upload -r pypitest
