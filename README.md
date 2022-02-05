# PowerAttackPublishingDB

## Setup:

**Prerequisites**

- GNU Make v4.2.1
- Docker Compose 1.29.1
- Docker 20.10.2

**Parse Data**

```bash
export SPELLS_DIR=data/spells/
export SPELLS_DATA_PATH=data/spells.csv
make spells
```

```bash
export MONSTERS_DIR=data/monsters/
export MONSTERS_DATA_PATH=data/monsters.csv
make monsters
```
**Load Data**

```bash
export POSTGRES_HOST=homebrew-db
export POSTGRES_DB=homebrew
export POSTGRES_USER=max
export POSTGRES_PASSWORD=<postgres-password>
make db-init

export DATA_PATH=data/spells.csv
export TABLE_NAME=spells
make db-write

make db-conn
```

**Query Data**

Sample queries:

```sql
SELECT
	name
	,school
	,components
FROM
	spells
WHERE level='3';

-- or

SELECT
	name
	,school
	,level
	,classes
FROM
	spells
WHERE
	classes ~ 'Cleric'
	AND range = 'Touch';
```
