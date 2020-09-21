import json

from ddlparse import DdlParse

sample_ddl = """
CREATE TABLE My_Schema.Sample_Table (
  Id integer PRIMARY KEY COMMENT 'User ID',
  Name varchar(100) NOT NULL COMMENT 'User name',
  Total bigint NOT NULL,
  Avg decimal(5,1) NOT NULL,
  Point int(10) unsigned,
  Zerofill_Id integer unsigned zerofill NOT NULL,
  Created_At date, -- Oracle 'DATE' -> BigQuery 'DATETIME'
  UNIQUE (NAME)
);
"""


# parse pattern (1-1)
table = DdlParse().parse(sample_ddl)

# parse pattern (1-2) : Specify source database
table = DdlParse().parse(ddl=sample_ddl, source_database=DdlParse.DATABASE.oracle)


# parse pattern (2-1)
parser = DdlParse(sample_ddl)
table = parser.parse()

print("* BigQuery Fields * : normal")
print(table.to_bigquery_fields())


# parse pattern (2-2) : Specify source database
parser = DdlParse(ddl=sample_ddl, source_database=DdlParse.DATABASE.oracle)
table = parser.parse()


# parse pattern (3-1)
parser = DdlParse()
parser.ddl = sample_ddl
table = parser.parse()

# parse pattern (3-2) : Specify source database
parser = DdlParse()
parser.source_database = DdlParse.DATABASE.oracle
parser.ddl = sample_ddl
table = parser.parse()

print("* BigQuery Fields * : Oracle")
print(table.to_bigquery_fields())


print("* TABLE *")
print("schema = {} : name = {} : is_temp = {}".format(table.schema, table.name, table.is_temp))

print("* BigQuery Fields *")
print(table.to_bigquery_fields())

print("* BigQuery Fields - column name to lower case / upper case *")
print(table.to_bigquery_fields(DdlParse.NAME_CASE.lower))
print(table.to_bigquery_fields(DdlParse.NAME_CASE.upper))

print("* COLUMN *")
for col in table.columns.values():
    col_info = {}

    col_info["name"]                  = col.name
    col_info["data_type"]             = col.data_type
    col_info["length"]                = col.length
    col_info["precision(=length)"]    = col.precision
    col_info["scale"]                 = col.scale
    col_info["is_unsigned"]           = col.is_unsigned
    col_info["is_zerofill"]           = col.is_zerofill
    col_info["constraint"]            = col.constraint
    col_info["not_null"]              = col.not_null
    col_info["PK"]                    = col.primary_key
    col_info["unique"]                = col.unique
    col_info["auto_increment"]        = col.auto_increment
    col_info["distkey"]               = col.distkey
    col_info["sortkey"]               = col.sortkey
    col_info["encode"]                = col.encode
    col_info["default"]               = col.default
    col_info["character_set"]         = col.character_set
    col_info["bq_legacy_data_type"]   = col.bigquery_legacy_data_type
    col_info["bq_standard_data_type"] = col.bigquery_standard_data_type
    col_info["comment"]               = col.comment
    col_info["description(=comment)"] = col.description
    col_info["bigquery_field"]        = json.loads(col.to_bigquery_field())

    print(json.dumps(col_info, indent=2, ensure_ascii=False))

print("* DDL (CREATE TABLE) statements *")
print(table.to_bigquery_ddl())

print("* DDL (CREATE TABLE) statements - dataset name, table name and column name to lower case / upper case *")
print(table.to_bigquery_ddl(DdlParse.NAME_CASE.lower))
print(table.to_bigquery_ddl(DdlParse.NAME_CASE.upper))

print("* Get Column object (case insensitive) *")
print(table.columns["total"])
print(table.columns["total"].data_type)