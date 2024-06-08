BEGIN;
CREATE TABLE IF NOT EXISTS Bookmark (
  isin TEXT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS Security (
  isin TEXT PRIMARY KEY,
  secid TEXT,
  gosreg TEXT,
  emitent_inn TEXT,
  emitent_title TEXT,
  type TEXT,
  name TEXT,
  shortname TEXT,
  marketprice_boardid TEXT
);
CREATE TABLE IF NOT EXISTS Emitent (
  emitent_inn TEXT PRIMARY KEY,
  sector TEXT
);
COMMIT;
