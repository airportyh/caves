CREATE TABLE cave (
  id SERIAL PRIMARY KEY,
  type_id INTEGER, -- moved siting type_id to cave_type_id
  name TEXT,
  number INTEGER);

CREATE TABLE cave_type ( -- renamed type to cave_type
  id SERIAL PRIMARY KEY,
  name TEXT);

CREATE TABLE architecture (
  id SERIAL PRIMARY KEY,
  name TEXT,
  chinese_name TEXT
);
  
CREATE TABLE iconography (
  id SERIAL PRIMARY KEY,
  type_id INTEGER,
  name TEXT,
  chinese_name TEXT
);

CREATE TABLE iconography_type ( -- added icon type for "Architectural Elements", "Inscriptions", "Ceiling types", etc
  id SERIAL PRIMARY KEY,
  name TEXT,
  chinese_name TEXT
);

CREATE TABLE siting (
  id SERIAL PRIMARY KEY,  -- added id for siting (SERIAL is an INTEGER file tha automatically increments)
  cave_id INTEGER, 
  iconography_id INTEGER, 
              -- moved type_if from here to cave.cave_type_id
  architecture_id INTEGER
);