
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
            named = filename.split(".")[0]
            f.append(named)
    return tuple(f)


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
        s = "type:{0} name:{1} table:{2} rootpage:{3} sql:{4}".format(*row) 
        repl.append(s)
    conn.close()
    return repl


def dbtable(name, table, ddl):
    conn = sqlite3.connect(fullname(name))
    c = conn.cursor()
    c.execute(ddl)
    conn.commit()
    conn.close()


def dbinsert(name, dml, values):
    print("dbinsert name:", name)
    print("dbinsert dml:", dml)
    print("dbinsert values:", values)
    conn = sqlite3.connect(fullname(name))
    c = conn.cursor()
    print("dbinsert pre exec")
    c.execute(dml, list(values))
    print("dbinsert post exec")
    conn.commit()
    print("dbinsert post commit")
    conn.close()
    print ("dbinsert did not raise error?")

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

