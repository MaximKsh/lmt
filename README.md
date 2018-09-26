# lmt
Lightweight Migration Tool - easy tool for database migration.

## Usage

`python3 lmt.py --help`

`python3 lmt.py --file conf.json`

* adapter - module name from 'adapters' folder which provides interface to database
* connection_string - connection_string to database
* direction - forward/backward
* target(int) - number of migration
* mirgration_path - root path for migration directories

Migration path should look like this:

```
├── migration_0
│   ├── 1_table1.sql
│   └── 2_table2.sql
├── migration_1
│   ├── 1_table3.sql
│   └── 2_table4.sql
└── migration_2
    ├── 1_table5.sql
    └── 2_table6.sql

```

Each of .sql file shoud contain forward block and backward block.
For example:
``` sql
-- forward begin

create table t5 (
    id SERIAL PRIMARY KEY,
    name TEXT
);

-- forward end

-- backward begin

drop table t5;

-- backward end

```


