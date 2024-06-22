# -*- coding: utf-8 -*-
#__all__: list = []

if "Tools.py" in __file__:
    from ctypes import *
    from typing import Any ,Self ,NoReturn ,Callable ,NewType
    from tkinter.messagebox import showerror

ctype: NewType = NewType("ctype" ,Any)

class SqStack(Structure):
    
    _fields_: tuple = (
                ("data" ,POINTER(c_int)) ,
                ("top" ,c_int) ,
                ("base" ,c_int)
            )

class DLL(object):

    Memory: dict[Callable:bool] = {}

    dirpath: str = '//'.join(__file__.split('\\')[:-1]) + "//"

    def __init__(self ,dll: str) -> NoReturn:
        self.__dll: Any = WinDLL(dll)

    @property
    def function(self) -> Callable:
        return self.__dll

    def config(self ,
               target: Callable ,
               * ,
               res: ctype,
               args: list[ctype]
               ) -> bool:

        try:
            target.restype: ctype = res
            target.argtypes: list[ctype] = args
        except Exception as Error:
            showerror("错误" ,str(Error))
            return False
        return True


if __name__ == "__main__":
    dll: DLL = DLL(DLL.dirpath+r"dll\x64\Debug\dll.dll")
    test: Callable = dll.function.test
    dll.config(test ,res=c_int ,args=[c_int ,c_int])

    #print(test(100 ,200))

    data_array = (c_int * 10)()
    data_pointer = POINTER(c_int).from_buffer(data_array)

    stack: SqStack = SqStack(data_pointer ,0 ,0)

    SqStackInit: Callable = dll.function.SqStackInit
    SqStackPop: Callable = dll.function.SqStackPop
    SqStackPush: Callable = dll.function.SqStackPush

    dll.config(SqStackInit ,res=c_int ,args=[POINTER(SqStack) ,c_int])
    dll.config(SqStackPop ,res=c_int ,args=[POINTER(SqStack) ,POINTER(c_int)])
    dll.config(SqStackPush ,res=c_int ,args=[POINTER(SqStack) ,c_int])

    print(SqStackInit(byref(stack) ,10))

    for i in range(10):
        print(SqStackPush(byref(stack) ,c_int(i)) ,end=' ')
    else:
        print()

    for i in range(10):
        data: c_int = c_int(0)
        SqStackPop(byref(stack) ,byref(data))
        print(data.value)

    








    
