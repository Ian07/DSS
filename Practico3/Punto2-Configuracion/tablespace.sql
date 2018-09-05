CREATE TABLESPACE punto_dos_tablespace LOCATION '/home/matias/directorio-tablespace';

CREATE DATABASE db_pg_default
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_AR.UTF-8'
    LC_CTYPE = 'es_AR.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE DATABASE db_otro_tablespace
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_AR.UTF-8'
    LC_CTYPE = 'es_AR.UTF-8'
    TABLESPACE = punto_dos_tablespace
    CONNECTION LIMIT = -1;