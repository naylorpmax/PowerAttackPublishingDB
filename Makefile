IMAGE_NAME?=homebrew-py
IMAGE_VERSION?=0.0.1

.PHONY: build-image
build-image:	## build docker image
	docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .

.PHONY: db
db:	## create database
	docker rm -f /homebrew-db || true
	docker-compose up -d homebrew-db

.PHONY: db-init
db-init: db
	sleep 5 && docker exec -it \
		homebrew-db \
		psql "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}/${POSTGRES_DB}" \
		-f sql/db-init.sql

.PHONY: db-conn
db-conn: ## connect to database
	docker exec -it \
		homebrew-db \
		psql "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}/${POSTGRES_DB}"

.PHONY: db-write
db-write: ## write data to database
	docker-compose run \
		-e POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
		-e DATA_PATH="${DATA_PATH}" \
		-e TABLE_NAME="${TABLE_NAME}" \
		homebrew-write

.PHONY: spells
spells:	## parse spell files
	docker-compose run \
		-e SPELLS_DIR="${SPELLS_DIR}" \
		-e SPELLS_DATA_PATH=${SPELLS_DATA_PATH} \
		scripts/spells

.PHONY: monsters
monsters:	## parse monster files
	docker-compose run \
		-e MONSTERS_DIR="${MONSTERS_DIR}" \
		-e MONSTERS_DATA_PATH=${MONSTERS_DATA_PATH} \
		scripts/monsters
