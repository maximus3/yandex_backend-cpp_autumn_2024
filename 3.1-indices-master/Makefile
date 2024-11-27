build.base:
	docker build --platform="linux/amd64" -f deploy/base/Dockerfile -t fruits/service-base .

push.base:
	docker tag fruits/service-base registry.yandex-academy.ru/school/2024-10/backend/cpp/homeworks/3.1-indices/fruits/service-base:latest
	docker push registry.yandex-academy.ru/school/2024-10/backend/cpp/homeworks/3.1-indices/fruits/service-base:latest

build.local:
	docker build  --platform="linux/amd64" -f deploy/local/Dockerfile -t fruits/service-local .

build.ci:
	docker build  --platform="linux/amd64" -f deploy/ci/Dockerfile -t fruits/service-ci .

push.ci:
	docker tag fruits/service-ci registry.yandex-academy.ru/school/2024-10/backend/cpp/homeworks/3.1-indices/fruits/service-ci:latest
	docker push registry.yandex-academy.ru/school/2024-10/backend/cpp/homeworks/3.1-indices/fruits/service-ci:latest

build:
	make build.base
	make build.local

build.postgres:
	docker build -f deploy/postgres/Dockerfile -t fruits/store .

push.postgres:
	docker tag fruits/store registry.yandex-academy.ru/school/2024-10/backend/cpp/homeworks/3.1-indices/fruits/store:latest
	docker push registry.yandex-academy.ru/school/2024-10/backend/cpp/homeworks/3.1-indices/fruits/store:latest

run.postgres:
	docker run --name store -e POSTGRES_USER=user -e POSTGRES_PASSWORD=random -e POSTGRES_DB=homework -p 5432:5432 registry.yandex-academy.ru/school/2024-10/backend/cpp/homeworks/3.1-indices/fruits/store

up:
	docker-compose up -d

status:
	docker-compose ps

down:
	docker-compose down

create_db:
	docker-compose exec store psql "user=user password=random" -c "create database homework WITH ENCODING 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';"

restore_db:
	docker-compose exec -T store psql "dbname=homework user=user password=random" <dump.sql

dump_db:
	docker-compose exec -T store pg_dump "dbname=homework user=user password=random" >dump.sql

drop_db:
	docker-compose exec store psql "user=user password=random" -c "drop database homework;"

psql:
	docker-compose exec store psql "dbname=homework user=user password=random"

logs:
	docker-compose logs -f

test:
	docker-compose exec service pytest --durations=0

bash:
	docker-compose exec service bash
