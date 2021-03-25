CREATE TABLE IF NOT EXISTS ir.part (
    `backup_name` String,
    `host_name` String,
    `host_addr` String,
    `database` String,
    `table` String,
    `partition` String,
    `part` String,
    `action` UInt8 comment '0 if created, 1 if deleted',
    `ctime` DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/snowball/tables/ir/part', '{{ hostname }}')
PARTITION BY (backup_name)
ORDER BY tuple();
