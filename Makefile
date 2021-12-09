.PHONY:front
front:
	cd front;\
	npm run dev

.PHONY:backend
dev:
	cd backend;\
	python manage.py runserver 0:8088

worker:
	cd backend;\
	python daemon.py

make prod:
	uwsgi --ini conf/uwsgi.ini

make nginx:
	nginx -c /Users/houzhenying/PycharmProjects/sqlserver-project/conf/nginx.conf
