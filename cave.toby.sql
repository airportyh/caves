CREATE TABLE cave (
  id INTEGER PRIMARY KEY,
  cave_type id INTEGER, -- moved siting type_id to cave_type_id
  name TEXT,
  number INTEGER);

CREATE TABLE cave_type ( -- renamed type to cave_type
  id INTEGER PRIMARY KEY,
  type_name TEXT);

CREATE TABLE architecture (
  id INTEGER PRIMARY KEY,
  location_description TEXT,
  chinese_location_description TEXT
);
  
CREATE TABLE icon (
  id INTEGER PRIMARY KEY,
  icon_type_id INTEGER,
  name TEXT,
  chinese_name TEXT
);

CREATE TABLE icon_type { -- added icon type for "Architectural Elements", "Inscriptions", "Ceiling types", etc
  id INTEGER PRIMARY KEY,
  name TEXT,
  chinese_name TEXT
};

CREATE TABLE siting (
  id SERIAL,  -- added id for siting (SERIAL is an INTEGER file tha automatically increments)
  cave_id INTEGER, 
  icon_id INTEGER, 
              -- moved type_if from here to cave.cave_type_id
  architecture_id INTEGER
);