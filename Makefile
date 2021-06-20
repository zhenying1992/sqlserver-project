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