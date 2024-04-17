prod-up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-up-build:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Press Ctrl + Z to make it a background process, but "exit" finishes the process instead of logout
prod-up-attached:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up

prod-up-build-attached:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build

prod-stop:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml stop

reload-nginx:
	docker exec -it hubble-nginx service nginx reload

bash:
	docker exec -it hubble bash

shell:
	docker exec -it hubble ./manage.py shell

makemigrations:
	docker exec -it hubble ./manage.py makemigrations

migrate:
	docker exec -it hubble ./manage.py migrate

initialfixture:
	docker exec -it hubble ./manage.py loaddata initial

demofixture:
	docker exec -it hubble ./manage.py loaddata demo

missingmigrations:
	docker exec -it hubble ./manage.py makemigrations payment app_plugins django_mailman tieredweight

fasttest:
	docker exec -it hubble coverage run --rcfile=.coveragerc-parallel manage.py test --no-input --keepdb --parallel --failfast

testtag:
	docker exec -it hubble ./manage.py test --noinput --tag=$(tag)

testapp:
	docker exec -it hubble ./manage.py test $(app) --noinput -v 3

test:
	docker exec -it hubble coverage run manage.py test --no-input

test-and-report: test cov-report

fast-and-report: fasttest cov-combine-report

cov-report:
	docker exec -it hubble coverage report

cov-report-html:
	docker exec -it hubble coverage html

cov-combine-report:
	docker exec -it hubble coverage combine
	docker exec -it hubble coverage report

statics:
	docker exec -it hubble ./manage.py collectstatic --noinput

makemessages:
	docker exec -it hubble django-admin makemessages

compilemessages:
	docker exec -it hubble django-admin compilemessages

sass:
	node-sass ./components/scss/hubble.scss ./spacetelescope/static/css/hubble.css

youtube-token:
	docker exec -it hubble python ./scripts/youtube-token.py
