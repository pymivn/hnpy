all: run

slackzip:
	./packer.sh

sitezip:
	rm -f pyhn.zip && zip -r pyhn.zip *.py hnpy

ls:
	aws lambda list-functions | jq '.Functions | .[].FunctionName'

deploy:
	aws lambda update-function-code --function-name ${APP} --zip-file fileb://${APP}.zip
run:
	# Can be timeout as default HTTP timeout = 60, job run > that
	aws lambda invoke --function-name ${APP} log

ci:
	flake8 --exclude template.py *.py hnpy/
	python cli.py
