class DB:
    def __init__(self, conn):
        self.conn = conn
        self.exist_queries = {
            "USER" : "SELECT USERNAME FROM USERS"
        }
    def exists(self, query_name, **kargs):
        c = self.conn.cursor()
        q = self.exist_queries[query_name]
        search_params = ["{} = ?".format(x,kargs[x]) for x in kargs]
        if (len(search_params) > 0):
            q += " WHERE {}".format(" AND ".join(search_params))
        # since the last python update we can now
        # assume kargs are ordered :D
        c.execute(q,tuple(kargs.values()))
        if c.fetchone():
            return True
        return False
