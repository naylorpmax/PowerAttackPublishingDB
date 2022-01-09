DROP TABLE IF EXISTS spells;
CREATE TABLE spells (
	name TEXT CONSTRAINT spells_pk PRIMARY KEY
	,level TEXT
	,school TEXT
	,casting_time TEXT
	,range TEXT
	,components TEXT
	,duration TEXT
	,classes TEXT
	,description TEXT
);
