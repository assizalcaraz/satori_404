# Makefile

init-chroma:
	./init_chroma_model.sh

up:
	docker-compose up --build -d

down:
	docker-compose down

rebuild:
	docker-compose down
	docker-compose build
	docker-compose up -d

start: init-chroma up
