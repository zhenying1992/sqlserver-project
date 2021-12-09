.PHONY:front
front:
	cd front;\
	npm run dev

.PHONY:backend
backend:
	cd backend;\
	python manage.py runserver 0:8088

worker:
	cd backend;\
	python daemon.py

make prod:
	uwsgi --ini uwsgi.ini

make nginx:
	nginx -c /Users/houzhenying/Desktop/sqlserver-project/nginx.conf