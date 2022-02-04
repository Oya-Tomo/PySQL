from const import ConstMeta
from column import Column, ColumnTypes
import sys

class Table:
    """
    # description
        This class can be used to define a table object.
    # table_name
        name of table
    # table_json
        Please set {"column_name": ColumnType} dict object in table_json.
    """
    def __init__(self, table_name: str, column_list: list):
        self.table_name = table_name
        self.column_list = column_list

        if len(column_list) == 0:
            print("ColumnError: This table has no columns !", file=sys.stderr)
            sys.exit()

    def to_sql(self):
        column_str_list = [item.to_sql() for item in self.column_list]
        table = f"{self.table_name}({', '.join(column_str_list)})"
        return table

if __name__ == "__main__":

    test_table = Table(
        "users",
        [
            Column("uid", ColumnTypes.STR, primary_key=True),
            Column("name", ColumnTypes.STR, not_null=True),
            Column("email", ColumnTypes.STR, unique=True),
            Column("age", ColumnTypes.INT, default=True, default_value=1),
            Column("phone", ColumnTypes.STR, default=True, default_value="unko")
        ]
    )

    print(test_table.to_sql())