PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS control_meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS auth_nonces(nonce TEXT PRIMARY KEY,used_at INTEGER NOT NULL,
 app_ref TEXT NOT NULL,account_ref TEXT NOT NULL,purpose TEXT NOT NULL,assertion_hash TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS erased_entities(entity_ref TEXT PRIMARY KEY,case_ref TEXT NOT NULL,erased_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS policies(
 epoch INTEGER PRIMARY KEY,entity_ref TEXT NOT NULL,purpose TEXT NOT NULL,state TEXT NOT NULL,
 effective_at INTEGER NOT NULL,observed_at INTEGER NOT NULL,source_ref TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS deletions(
 id TEXT PRIMARY KEY,entity_ref TEXT NOT NULL,requested_at INTEGER NOT NULL,effective_at INTEGER NOT NULL,
 epoch INTEGER NOT NULL,source_ref TEXT NOT NULL,training_disposition TEXT NOT NULL,state TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS deletion_sinks(
 case_ref TEXT NOT NULL REFERENCES deletions(id),sink TEXT NOT NULL,status TEXT NOT NULL,
 acknowledged_at INTEGER,source_ref TEXT,PRIMARY KEY(case_ref,sink));
