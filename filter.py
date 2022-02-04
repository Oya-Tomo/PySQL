import sys
from column import ColumnTypes

class Or:
    def __init__(self, formula_list):
        self.formula_list = formula_list

class Equal:
    def __init__(self, column_name, value):
        self.column_name = column_name
        self.value = value
        if type(self.value) == str:
            self.column_type == ColumnTypes.STR
        elif type(self.value) == int:
            self.column_type == ColumnTypes.INT
        elif type(self.value) == float:
            self.column_type == ColumnTypes.FLOAT
        elif type(self.value) == bytes:
            self.column_type == ColumnTypes.BYTE
        elif self.value == None:
            self.column_type = ColumnTypes.NONE
        else :
            print("ConpareValueError : This value type is not supported.", file=sys.stderr)

    def to_sql(self):
        if self.column_type == ColumnTypes.STR:
            