CREATE TABLE quotes (
  id TEXT PRIMARY KEY,
  text TEXT NOT NULL,
  author TEXT NOT NULL,
  category TEXT,
  tags TEXT
);

INSERT INTO quotes VALUES ('example-uuid', 'The only way to do great work...', 'Steve Jobs', 'Motivation', 'work,life');