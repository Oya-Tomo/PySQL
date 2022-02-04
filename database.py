import sqlite3
import sys
from table import Table
from column import Column, ColumnTypes

class DataBase:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.connect = sqlite3.connect(file_name)
        self.cursor = self.connect.cursor()

    def commit(self):
        self.connect.commit()
        self.cursor = self.connect.cursor()

    def create_table(self, table: Table):
        text = table.to_sql()
        sql = f"create table if not exists {text};"
        print(sql)
        self.cursor.execute(sql)
        self.commit()

    def delete_table(self, table_name: str):
        if table_name in self.get_table_names():
            sql = f"drop table {table_name};"
            self.cursor.execute(sql)
            self.commit()
        else:
            print("TableError : no such a table. (in delete_table())", file=sys.stderr)

    def rename_table(self, old_name: str, new_name: str):
        if old_name in self.get_table_names():
            sql = f"alter table {old_name} rename to {new_name};"
            self.cursor.execute(sql)
            self.commit()
        else:
            print("TableError : no such a table. (in rename_table())", file=sys.stderr)


    def get_table_names(self):
        sql = "select name from sqlite_master where type='table';"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        table_names = [item[0] for item in res]
        return table_names

    def get_table_info(self, table_name: str):
        if table_name in self.get_table_names():
            sql = f"pragma table_info ({table_name});"
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            columns = []
            for item in res:
                column = {"table_name": item[1], "type": item[2], "default": item[4]}
                if item[3] == 1:
                    column["not_null"] = True
                else:
                    column["not_null"] = False
                if item[5] == 1:
                    column["primary_key"] = True
                else:
                    column["primary_key"] = False
                columns.append(column)

            return columns
        else:
            print("TableError : no such a table. (in get_table_info())", file=sys.stderr)
            return []

    def insert_data(self, table_name: str, data_json: dict):
        columns = list(data_json.keys())
        fields = list(data_json.values())

        sql = f"insert into {table_name}({', '.join(columns)}) values({', '.join(['?']*len(columns))});"
        self.cursor.execute(sql, fields)
        self.commit()

    def select_data(self, table_name: str, where: str=None, order_by: str=None, limit: int=None):
        sql = f"select * from {table_name}"
        if where != None:
            sql += f" where {where}"
        if order_by != None:
            sql += f" order by {order_by}"
        if limit != None:
            sql += f" limit {limit}"
        sql += ";"
        
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.commit()

        return res

    def update_data(self, table_name: str, data_json: dict, where: str=None):
        columns = [f"{key}=?" for key in data_json.keys()]        
        sql = f"update {table_name} set {', '.join(columns)}"
        if where != None:
            sql += f" where {where}"
        sql += ";"

        self.cursor.execute(sql, list(data_json.values()))
        self.commit()

    def delete_data(self, table_name: str, where: str=None):
        sql = f"delete from {table_name}"
        if where != None:
            sql += f" where {where}"

        self.cursor.execute(sql)
        self.commit()



if __name__ == "__main__":
    import pprint

    db = DataBase("test/test.db")

    test_table = Table(
        "users",
        [
            Column("name", ColumnTypes.STR, unique=True),
            Column("age", ColumnTypes.INT, not_null=True)
        ]
    )
    # db.delete_table(test_table.table_name)



    db.create_table(test_table)
    # db.rename_table(test_table.table_name+" ", "people")
    print(db.get_table_names())
    pprint.pprint(db.get_table_info(test_table.table_name))
    db.insert_data(test_table.table_name, {"name": "taka", "age": 67})
    db.insert_data(test_table.table_name, {"name": "saku", "age": 67})
    db.insert_data(test_table.table_name, {"name": "saka", "age": 66})
    db.insert_data(test_table.table_name, {"name": "tomo", "age": 16})
    db.insert_data(test_table.table_name, {"name": "yuka", "age": 41})
    db.insert_data(test_table.table_name, {"name": "mariko", "age": 70})

    res = db.select_data(test_table.table_name, where="age = 67",order_by="name asc")
    print(res)

    db.update_data(test_table.table_name, {"name": "oya-tomo"}, where="age=16")
    db.delete_data(test_table.table_name, where="age=67")
