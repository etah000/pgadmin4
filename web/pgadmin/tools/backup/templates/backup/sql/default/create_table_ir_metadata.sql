CREATE TABLE IF NOT EXISTS ir.metadata (
    `backup_name` String,
    `host_name` String,
    `host_addr` String,
    `data` String,
    `ctime` DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/snowball/tables/ir/metadata', '{{ hostname }}')
PARTITION BY (backup_name,host_name,host_addr)
ORDER BY tuple();
