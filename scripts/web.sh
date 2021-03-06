#!/bin/bash

# a test script to run queries against the web server
#
BASEURL="http://127.0.0.1:5000"

# exit on error
set -e

bah() {
curl -s -X POST $BASEURL -T - <<EOF
{
  "name": "bob",
  "number": 23
}
EOF
exit
}

json() {
curl -s -X POST \
	-H "Content-Type: application/json" \
	$BASEURL/sqlite/v1/db/create -d @- <<EOF
{
  "name": "bob",
  "number": 23
}
EOF
}

sql() {
curl -s -X POST \
	-H "Content-Type: application/sql" \
	$BASEURL/sqlite/v1/db/create/pookie -d @- <<EOF
create table test01 (
id integer primary key,
name text
);
EOF
}

say() { echo ">>> $@"; }

list() {
    say "list dbs"
    curl -s $BASEURL/sqlite/v1/db/list 
    say 
}

schema() {
    say "db schema"
    curl -s $BASEURL/sqlite/v1/db/pookie/schema 
    say
}

## DUPE OF sql()
table() {
    say "make table"
    curl -s \
         -X POST \
	       -H "Content-Type: application/sql" \
	      $BASEURL/sqlite/v1/db/pookie/create -d @- \
<<EOF
create table if not exists test01 (
id integer primary key,
name text
);
EOF
    say "the table is made"
}


insertXXX() {
    say "insert into table: test01"
    curl -X POST \
	-H "Content-Type: application/json" \
	$BASEURL/sqlite/v1/db/pookie/insert/test01 -d @- <<EOF
{"query": "insert into test01 (name) values (?)", "values":["only"]} 
EOF
    say "table is inserted"
}

insert() {
    say "insert into table"
    curl -s -X POST \
	-H "Content-Type: application/json" \
	$BASEURL/sqlite/v1/db/pookie/insert -d @- <<EOF
{
   "query": "insert into test01 (name) values (?)",
   "values": [
      ["first"],
      ["other"],
      ["quad"],
      ["aha"]
    ]
}
EOF
    say "table is inserted"
}

selected() {
    say "select from table"
    curl -s \
	-H "Content-Type: application/json" \
	$BASEURL/sqlite/v1/db/pookie/table/test01 
    say "table is selected"
}

sql       # create db
table     # create table in db
#list
#schema
insert    # insert rows into table
selected  # query rows in table
