from sqlalchemy import create_engine, select, func, text

# create engine to connect to database


def find_max_uid():
    engine = create_engine('sqlite:///newpipe.db', echo=True)

    # connect to database
    conn = engine.connect()

    # get the maximum uid from the streams table
    query = text('SELECT MAX(uid) FROM streams')
    result = conn.execute(query).fetchone()

    max_uid = result[0]

    # close the database connection
    conn.close()

    # print the maximum uid
    return max_uid
