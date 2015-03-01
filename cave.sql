CREATE TABLE cave (id INTEGER PRIMARY KEY,
		name TEXT,
		number INTEGER);

CREATE TABLE type (id INTEGER PRIMARY KEY,
		type_name TEXT);
		
CREATE TABLE icon (
  id INTEGER PRIMARY KEY,
	name TEXT,
  chinese_name TEXT
);

CREATE TABLE architecture (
  id INTEGER PRIMARY KEY,
	location_description TEXT,
  chinese_location_description TEXT
);

CREATE TABLE siting (cave_id INTEGER, 
			type_id INTEGER, icon_id INTEGER, 
			architecture_id INTEGER);