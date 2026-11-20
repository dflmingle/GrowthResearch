PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS namespaces(
 id TEXT PRIMARY KEY, tenant TEXT NOT NULL, issuer TEXT NOT NULL, app TEXT NOT NULL,
 sector TEXT NOT NULL, entity_type TEXT NOT NULL CHECK(entity_type IN('person','account','device','app_instance','household')),
 scope TEXT NOT NULL, version TEXT NOT NULL, evidence TEXT NOT NULL,
 UNIQUE(tenant,issuer,app,sector,entity_type,scope,version));
CREATE TABLE IF NOT EXISTS namespace_mappings(
 a TEXT NOT NULL REFERENCES namespaces(id), b TEXT NOT NULL REFERENCES namespaces(id),
 purpose TEXT NOT NULL, evidence TEXT NOT NULL, observed_at INTEGER NOT NULL,
 PRIMARY KEY(a,b,purpose));
CREATE TABLE IF NOT EXISTS entities(
 id TEXT PRIMARY KEY, namespace_id TEXT NOT NULL REFERENCES namespaces(id), token TEXT,
 entity_type TEXT NOT NULL, created_at INTEGER NOT NULL, deleted INTEGER NOT NULL DEFAULT 0,
 UNIQUE(namespace_id,token));
CREATE TABLE IF NOT EXISTS edge_revisions(
 id TEXT NOT NULL, revision INTEGER NOT NULL, src TEXT NOT NULL REFERENCES entities(id),
 dst TEXT NOT NULL REFERENCES entities(id), kind TEXT NOT NULL,
 grain TEXT NOT NULL, source_ref TEXT NOT NULL, scope TEXT NOT NULL,
 confidence REAL, quality_kind TEXT NOT NULL, quality_scope TEXT NOT NULL,
 method_version TEXT NOT NULL, status TEXT NOT NULL,
 valid_from INTEGER NOT NULL, valid_to INTEGER, observed_at INTEGER NOT NULL,
 available_at INTEGER NOT NULL, revoked_at INTEGER, purpose TEXT NOT NULL,
 policy_epoch INTEGER NOT NULL, graph_version INTEGER NOT NULL,
 PRIMARY KEY(id,revision));
CREATE TABLE IF NOT EXISTS events(
 id TEXT PRIMARY KEY, tenant TEXT NOT NULL, app_ref TEXT NOT NULL REFERENCES entities(id),
 source TEXT NOT NULL, source_event_id TEXT NOT NULL, revision INTEGER NOT NULL,
 event_type TEXT NOT NULL, account_ref TEXT REFERENCES entities(id),
 occurred_at INTEGER NOT NULL, received_at INTEGER NOT NULL, observed_at INTEGER NOT NULL,
 available_at INTEGER NOT NULL, source_ref TEXT NOT NULL, purpose TEXT NOT NULL,
 policy_epoch INTEGER NOT NULL, payload_hash TEXT NOT NULL, payload_json TEXT,
 deleted INTEGER NOT NULL DEFAULT 0,
 UNIQUE(tenant,app_ref,source,source_event_id,revision));
CREATE TABLE IF NOT EXISTS ledger(
 id TEXT PRIMARY KEY, event_ref TEXT NOT NULL REFERENCES events(id),
 app_ref TEXT NOT NULL REFERENCES entities(id), account_ref TEXT REFERENCES entities(id),
 source TEXT NOT NULL, economic_key TEXT NOT NULL, revision INTEGER NOT NULL,
 amount_micros INTEGER, currency TEXT NOT NULL, economic_kind TEXT NOT NULL,
 economic_at INTEGER NOT NULL, occurred_at INTEGER NOT NULL, observed_at INTEGER NOT NULL,
 available_at INTEGER NOT NULL, correction_of TEXT REFERENCES ledger(id),
 semantic_hash TEXT NOT NULL, deleted INTEGER NOT NULL DEFAULT 0,
 UNIQUE(app_ref,source,economic_key,revision));
CREATE TABLE IF NOT EXISTS outbox(id TEXT PRIMARY KEY,event_ref TEXT NOT NULL,payload_json TEXT,status TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS coverage(
 id TEXT PRIMARY KEY, app_ref TEXT NOT NULL REFERENCES entities(id),
 start_at INTEGER NOT NULL,end_at INTEGER NOT NULL,status TEXT NOT NULL,
 observed_at INTEGER NOT NULL,available_at INTEGER NOT NULL,source_ref TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS feature_bundles(
 id TEXT PRIMARY KEY,subject_ref TEXT NOT NULL,purpose TEXT NOT NULL,as_of INTEGER NOT NULL,
 since_at INTEGER NOT NULL,materialized_at INTEGER NOT NULL,available_at INTEGER NOT NULL,
 graph_version INTEGER NOT NULL,policy_epoch INTEGER NOT NULL,
 lineage_json TEXT NOT NULL,values_json TEXT,status TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS training_snapshots(
 id TEXT PRIMARY KEY,entity_refs_json TEXT NOT NULL,trained_model INTEGER NOT NULL,status TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS audit_log(
 seq INTEGER PRIMARY KEY AUTOINCREMENT,at INTEGER NOT NULL,kind TEXT NOT NULL,
 payload_json TEXT NOT NULL,previous_hash TEXT NOT NULL,hash TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS edge_lookup ON edge_revisions(src,dst,purpose,observed_at);
CREATE INDEX IF NOT EXISTS ledger_asof ON ledger(app_ref,observed_at,available_at);
