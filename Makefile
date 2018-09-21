# python's virtualenv should be activated before run 'boot'
boot:
	pip install -r requirements.txt & cd frontend && yarn install

dev:
	python manage.py runserver --settings=backend.dev_settings & cd frontend && yarn start