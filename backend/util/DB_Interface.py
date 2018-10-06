import sqlite3

class Stub:
    def __init__(self, conn_url, type, q):
        self.conn = sqlite3.connect(conn_url)
        self.q = q
        self.type = type
        self.q_values = tuple()

    def set(self, **kargs):
        if self.type != "UPDATE":
            raise Exception("Can not use 'SET' on a '{}' command".format(self.type))
        sets = ["{} = ?".format(x) for x in kargs]
        if (len(sets) > 0):
            self.q += " SET {}".format(", ".join(sets))
        self.q_values += tuple(kargs.values())
        return self

    def where(self, **kargs):
        search_params = ["{} = ?".format(x) for x in kargs]
        if (len(search_params) > 0):
            self.q += " WHERE {}".format(" AND ".join(search_params))
        self.q_values += tuple(kargs.values())
        return self

    def execute(self):
        c = self.conn.cursor()
        # since the last python update we can now
        # assume kargs are ordered :D
        c.execute(self.q,self.q_values)
        if (self.type == "EXISTS"):
            r = (c.fetchone() != None)
            self.conn.close()
            return r
        elif (self.type == "UPDATE"):
            self.conn.commit()
            r = None
            self.conn.close()
            return r
        raise Exception("Unknown Stub type '{}'".format(self.type))

    def __bool__(self):
        if (self.type == "EXISTS"):
            return self.execute()
        return True

class DB:
    def __init__(self):
        self.conn_url = "db/test.sqlite3"
        self.exist_queries = {
            "USER" : "SELECT USERNAME FROM USERS"
        }
        self.update_queries = {
            "USER" : "UPDATE USERS"
        }

    def exists(self, query_name, **kargs):
        s = Stub(self.conn_url, "EXISTS", self.exist_queries[query_name])
        return s
    def update(self, query_name, **kargs):
        s = Stub(self.conn_url, "UPDATE", self.update_queries[query_name])
        return s