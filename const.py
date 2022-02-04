class ConstMeta(type):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise TypeError(f"Can\'t rebind const : {name}")
        else :
            self.__setattr__(name, value)

if __name__ == "__main__":
    class MyValue(metaclass=ConstMeta):
        author = "OyaTomo.dev"
    