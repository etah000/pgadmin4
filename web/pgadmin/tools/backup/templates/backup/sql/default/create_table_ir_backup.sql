CREATE TABLE IF NOT EXISTS ir.backup
(
    `backup_name` String,
    `host_name` String,
    `host_addr` String,
    `backup_type` UInt8 comment '0 if full bacup, 1 if increment backup',
    `backup_deleted` UInt8 comment '1 if deleted else 0',
    `backup_ctime` DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/snowball/tables/ir/backup', '{{ hostname }}')
PARTITION BY tuple()
ORDER BY tuple();
