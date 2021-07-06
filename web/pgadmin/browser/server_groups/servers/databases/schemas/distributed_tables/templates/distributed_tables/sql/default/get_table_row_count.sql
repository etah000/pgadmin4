SELECT COUNT(*) FROM {{ conn|qtIdent(data.did, data.tid) }};
