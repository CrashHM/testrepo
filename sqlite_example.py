#!/usr/bin/env python3

#
# This file shows how to create a SQLite table in a file, store data in it,
# and run a query.
#
# The filename and table are set in the variables DBFILE and DBTABLE.
# An SQLite file can contain multiple tables.
#
# The table holds a series of (fake) retail products
# uniquely identified by a stock code.
#


import sqlite3

DBFILE = 'inventory.db'
DBTABLE = 'products'

# The list of products
plist = [
         # Product ID   # Description              # Quantity
         [ "85123A",    "Blue paisley tissue box", 8     ],
         [ "82578",     "Kitchen metal sign",      2     ],
         [ "22111",     "Small popcorn holder",    3     ],
         [ "23084",     "Rabbit night light",      8     ],
         [ "22776",     "Swallows greeting card",  4     ]
];

def load_db():
    print("Loading the database with %d items." % len(plist))

    # Open a connection the database
    con = sqlite3.connect(DBFILE)
    cur = con.cursor()

    #
    # Create the table if it's not there already
    #
    # The table has 3 columns, each with a data type associated:
    # - productID - unique product identifier, which is a TEXT type (string)
    # - description - a human-readable description, which is a TEXT type (string)
    # - quantity - amount of inventory, which a whole number (integer)
    #
    # Here, the table is dropped (deleted) first just to show an example.
    #
    cur.execute("DROP TABLE %s" % DBTABLE)
    cur.execute("CREATE TABLE IF NOT EXISTS %s (productID TEXT PRIMARY KEY,"
                "description TEXT, quantity INTEGER);" % DBTABLE)

    # Adding the data can be done multiple ways:
    # 1) Row-by-row, looping through the list
    # 2) All at once using executemany(), which is best for inserting many rows at a time.
    # This example uses #2, requiring that we pass a list-of-lists to executemany()
    # where each list is of the format [ productID, description, quantity ] for an item.
    cur.executemany("INSERT INTO %s "
                    "(productID, description, quantity) "
                    "VALUES (?, ?, ?)" % DBTABLE, plist)

    # This causes the above change to be flushed to the file.
    con.commit()

    # We are done with the database for now.
    con.close()

def run_query():
    # Open the database again
    con = sqlite3.connect(DBFILE)
    cur = con.cursor()

    #
    # Make a LIKE query for a description.  We use a SELECT command for this and
    # specify the field of interest.   For full syntax:  https://sqlite.org/lang_select.html
    # Placing the '%' character at both ends of the search string means that the match
    # will occur if the string appears anywhere within the description column.
    #
    # To insert fields into the SQL command, use list with '?' in the string.  For example:
    # if you pass ?, ? in the string and do this: cur.execute("...", arg) it will be
    # substituted with arg1[0] and arg[1].
    #
    toSearch = "sign"
    qkey = ('%'+toSearch+'%', )
    recs = cur.execute("SELECT * FROM %s WHERE description LIKE ?" % DBTABLE, qkey)
    print("Records that match query 1: ")
    for r in recs:
        print("Product ID: %s" % r[0])
        print("Description: %s" % r[1])
        print("Quantity: %d" % r[2])

    # Here is an example of an exact match
    qkey = ("22776",)
    recs = cur.execute("SELECT * FROM %s WHERE productID = ?" % DBTABLE, qkey)
    print("Records that match query 2: ")
    for r in recs:
        print("Product ID: %s" % r[0])
        print("Description: %s" % r[1])
        print("Quantity: %d" % r[2])
    con.close()

def main():
    print("Loading the database...")
    load_db();
    print("Done.")
    print("Querying:")
    run_query()

if __name__ == "__main__":
    main()
