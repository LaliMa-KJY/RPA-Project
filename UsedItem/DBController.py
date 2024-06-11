import sqlite3

class DBController:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('crawling.db')

        curs = self.conn.cursor()
        sql = """
                CREATE TABLE IF NOT EXISTS ITEM(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flatform VARCHAR(10),
                    title VARCHR(200),
                    url VARCHAR(200),
                    location VARCHAR(200),
                    price BIGINT(20),
                    img_url VARCHAR(500)
                )
              """
        curs.execute(sql)
        self.conn.commit()
        curs.close()
    
    def __del__(self):
        self.conn.close()
    
    def saveItems(self, items):
        print(items)
        curs = self.conn.cursor()
        sql = """
                DELETE FROM ITEM
              """
        curs.execute(sql)

        sql = """
                INSERT INTO ITEM (flatform, title, url, location, price, img_url) VALUES (?, ?, ?, ?, ?, ?)
              """
        for i in items:
            curs.execute(sql, (i['flatform'], i['title'], i['url'], i['location'], i['price'], i['img_url']))
            self.conn.commit()