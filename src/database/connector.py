import mysql.connector


class SQLConnector:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="18.217.241.65",
            user="xiaojie",
            passwd="Zxj_691012",
            database="storm"
        )
        self.mycursor = self.mydb.cursor()
        # self.del_all()

    def del_all(self):
        self.mycursor.execute("delete from application")
        self.mydb.commit()

    def insert(self, index, YOLO_416_EX_TIME, YOLO_256_EX_TIME, YOLO_608_EX_TIME, YOLO_416_CPU, YOLO_256_CPU, YOLO_608_CPU, PROCESSING_LATENCY):
        sql = "INSERT INTO application VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (index, YOLO_416_EX_TIME, YOLO_256_EX_TIME, YOLO_608_EX_TIME, YOLO_416_CPU, YOLO_256_CPU, YOLO_608_CPU, PROCESSING_LATENCY)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def disconnect(self):
        self.mydb.disconnect()
        self.mydb.close()

    def get_last_index(self):
        self.mycursor.execute("SELECT * FROM application")
        result = self.mycursor.fetchall()
        if len(result) > 0:
            return result[-1][0]
        else:
            return 0

    def show(self):
        self.mycursor.execute("SELECT * FROM application")
        for x in self.mycursor:
            print(x)


if __name__ == "__main__":
    connector = SQLConnector()
    connector.del_all()
    #connector.show()
    #print(connector.get_last_index())
    #connector.disconnect()


