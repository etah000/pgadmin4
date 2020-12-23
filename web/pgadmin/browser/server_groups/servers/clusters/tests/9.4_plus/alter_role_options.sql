-- Role: "Role2_$%{}[]()&*^!@""'`\/#"
-- DROP ROLE "Role2_$%{}[]()&*^!@""'`\/#";

CREATE ROLE "Role2_$%{}[]()&*^!@""'`\/#" WITH
  NOLOGIN
  SUPERUSER
  INHERIT
  CREATEDB
  NOCREATEROLE
  NOREPLICATION
  CONNECTION LIMIT 100
  ENCRYPTED PASSWORD '<PASSWORD>'
  VALID UNTIL '<TIMESTAMPTZ_1>';

ALTER ROLE "Role2_$%{}[]()&*^!@""'`\/#" IN DATABASE postgres SET application_name TO 'pg4';

COMMENT ON ROLE "Role2_$%{}[]()&*^!@""'`\/#" IS 'This is detailed description';
