
import os, sqlite3

#from os import listdir

# TODO: namespace user files beyond the global
userfiles = "userdata"

def fullname(name):
    """ fullname returns the proper path to the database file """
    name += '.db'
    return os.path.join(userfiles, name)

def dbcreate(name):
    if not os.path.isdir(userfiles):
        os.mkdir(userfiles)
    conn = sqlite3.connect(fullname(name))
    conn.close()

def dblist():
    dir = userfiles
    f = []
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for filename in filenames:
            print("checking:", filename)
            named = filename.split(".")
            if ((len(named) > 1) and (named[1] == "db")):
                f.append(named[0]) 
    return tuple(f)


def dbtables(name):
    """
      returns a list of tables 
    """
    conn = sqlite3.connect(fullname(name))
    c = conn.cursor()

    query="select name from sqlite_master where type = 'table';"
    repl = [row[0] for row in c.execute(query)]
    conn.close()
    return repl

def dbschema(name):
    """
      returns a list of records with:
	  type text,
	  name text,
	  tbl_name text,
	  rootpage integer,
	  sql text
    """
    conn = sqlite3.connect(fullname(name))
    c = conn.cursor()

    query='select * from sqlite_master'
    repl = []
    for row in c.execute(query):
        s = "schema type:{0} name:{1} table:{2} rootpage:{3} sql:{4}".format(*row) 
        repl.append(s)
    conn.close()
    return repl

def db_table_info(dbname,table):
    """ TODO: parameterize / sanitize! """
    query = "pragma table_info({})".format(table)
    return db_query(dbname, query)

    conn = sqlite3.connect(fullname(dbname))
    c = conn.cursor()
    # returns cid, name, type, notnull, dflt_value, pk
    repl = [row for rows in c.execute(query)]
    conn.commit()
    conn.close()
    return repl

def dbtable(name, ddl):
    """create/alter/delete table"""
    conn = sqlite3.connect(fullname(name))
    c = conn.cursor()
    c.execute(ddl)
    conn.commit()
    conn.close()


def dbinsert(name, dml, values):
    print("dbinsert name:", name, "dml:", dml, "values:", values)
    conn = sqlite3.connect(fullname(name))
    c = conn.cursor()
    c.executemany(dml, list(values))
    conn.commit()
    conn.close()
    print ("dbinsert did not raise error!")

def dbselect(name, table):
    conn = sqlite3.connect(fullname(name))
    c = conn.cursor()
    repl = []
    query = "select * from {}".format(table)
    for row in c.execute(query):
        repl.append("\t".join([str(s) for s in row]))
    conn.commit()
    conn.close()
    return "\n".join(repl)

# table_info
# returns cid, name, type, notnull, dflt_value, pk
def db_query(dbname, query):
    conn = sqlite3.connect(fullname(dbname))
    c = conn.cursor()
    results = c.execute(query)
    #columns = [ results.description.name(i) for i in results.description.index ]
    columns = [ desc[0] for desc in results.description ]
    print("query column:", columns)
    rows = [row[:] for row in results]
    print("rows:", rows)
    conn.commit()
    conn.close()
    return columns, rows

def db_dumper(dbname):
    def generate():
        # how to return from sqlite.py instead? (close after stream!)
        conn = sqlite3.connect(fullname(dbname))
        for line in conn.iterdump():
            yield line + "\n"
        conn.close()

    return generate
