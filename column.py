import sys
from .const import ConstMeta

class ColumnTypes(metaclass=ConstMeta):
    """
    # description
        This class contains many constant values (the types of column values)
    # caution
        Do not make instance and rebind these values !!!
    """
    STR = "str"
    INT = "integer"
    FLOAT = "float"
    BYTE = "byte"
    NONE = "null"

class Column:
    """
    # description
        This class is for making columns settings.
    """
    def __init__(self, column_name: str, column_type: str, primary_key: bool=False, not_null: bool=False, unique: bool=False, default: bool=False, default_value=None):
        self.column_name = column_name
        self.column_type = column_type
        self.primary_key = primary_key
        self.not_null = not_null
        self.unique = unique
        self.default = default
        self.default_value = default_value

        if self.not_null: # not nullにデフォルトでNullを挿入しないため
            if self.default and self.default_value == None:
                print("NullError: You can\'t set NULL as default value in the not-null column.", file=sys.stderr)
                sys.exit()
        
        if self.primary_key: # Primary Keyの強制的なNull禁止と一意な値
            self.not_null = True
            self.unique = True
            
            if default:
                print("PrimaryKeyError: You can\'t set default value in the primary-key column.\nA primary-key value must be UNIQUE !", file=sys.stderr)
                sys.exit()

        if self.unique and default: # uniqueな値にデフォルトで値の代入を禁止する
            print("UniqueError: You can\'t set default value in the unique column.", file=sys.stderr)
            sys.exit()

        # デフォルト値にByteを代入する処理が出来ないため、それをかわす処理
        if self.default and self.column_type == ColumnTypes.BYTE and (type(self.default_value) == bytes or type(self.default_value) == bytearray):
            print("DefaultValueError: sorry. this package isn`t supporting the function to set BYTE or BLOB value as default.", file=sys.stderr)
            sys.exit()

        if self.default and self.default_value == None: # デフォルト値がNoneの場合
            pass
        elif self.default and self.column_type == ColumnTypes.STR and type(self.default_value) != str: # デフォルトの値の型が指定と異なるとき
            print("DefaultValueError : default value type is incorrect.")
            sys.exit()
        elif self.default and self.column_type == ColumnTypes.INT and type(self.default_value) != int:
            print("DefaultValueError : default value type is incorrect.")
            sys.exit()
        elif self.default and self.column_type == ColumnTypes.FLOAT and type(self.default_value) != float:
            print("DefaultValueError : default value type is incorrect.")
            sys.exit()
        elif self.default and self.column_type == ColumnTypes.BYTE and self.default_value != None:
            print("DefaultValueError : default value type is incorrect.")
            sys.exit()


    def to_sql(self): # カラムをSQL文で使用できるように出力
        column = f"{self.column_name} {self.column_type}"

        if self.primary_key:
            column += " primary key not null"
            return column
        else:
            if self.not_null:
                column += " not null"
            if self.unique:
                column += " unique"
            if self.default:
                if self.column_type == ColumnTypes.INT or self.column_type == ColumnTypes.FLOAT:
                    column += f" default {self.default_value}"
                elif self.column_type == ColumnTypes.STR:
                    column += f" default \"{self.default_value}\""

        return column

if __name__ == "__main__":
    column = Column("test", ColumnTypes.INT, not_null=True, default=True, default_value="unko")
    column = Column("test", ColumnTypes.INT, not_null=True)
    print(column.to_sql())