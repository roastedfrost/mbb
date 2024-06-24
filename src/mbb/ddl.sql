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
CREATE TABLE IF NOT EXISTS SecurityData (
  isin TEXT PRIMARY KEY,
  secid TEXT,
  issuesize INTEGER,
  issuesizeplaced INTEGER,
  settledate TEXT,
  couponpercent REAL,
  couponvalue REAL,
  nextcoupon TEXT,
  couponperiod INTEGER,
  accruedint REAL,
  facevalue REAL,
  facevalueonsettledate REAL,
  matdate TEXT,
  offerdate TEXT,
  buybackprice REAL,
  buybackdate TEXT
);
CREATE TABLE IF NOT EXISTS Emitent (
  emitent_inn TEXT PRIMARY KEY,
  sector TEXT
);
COMMIT;
