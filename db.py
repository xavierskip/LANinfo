import sqlite3

class database:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.cur = self.db.cursor()
    def __del__(self):
        self.close()
    def commit(self):
        self.db.commit()
    def close(self):
        if hasattr(self,"db"):
            self.db.close()
    def create_table(self,schame,tablename):
        with open(schame) as sql:
            schema = sql.read().format(table=tablename)
            self.cur.executescript(schema)
            self.commit()
    def initTable(self,schame,tablename,iplist):
        self.create_table(schame,tablename)
        sql = "INSERT INTO `%s` (ip) VALUES (?)" %tablename
        ips = [ (i,) for i in iplist]
        self.cur.executemany(sql,ips)
        self.commit()

################### don't use it 
def update(db,tablename):
    with open(config['INFO'],'r') as f:
        rows = []
        for l in f.readlines():
            ip,mac,comment,name = l.decode('utf-8')[:-1].split('|')
            rows.append((mac,comment,name,ip))
        sql = "UPDATE `%s` SET mac=?,comment=?,name=? WHERE ip=?" %tablename
        db.cur.executemany(sql,rows)
        db.commit()