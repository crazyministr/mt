# -*- coding: utf-8 -*-


class JVMInstructions(object):
    """
        LOAD_<x>  - положить на стек значение переменной x
        STORE_<x> - сохранить в переменной x значение с вершины стека
        CONST_<n> - положить число n на вершину стека
        POP       - удалить число с вершины стека
        ADD       - сложить два числа на вершине стека
        SUB       - вычесть два числа на вершине стека
        LT        - сравнить два числа с вершины стека (a < b). Результат - 0 или 1
        JZ <a>    - если на вершине стека 0 - перейти к адресу a.
        JNZ <a>   - если на вершине стека не 0 - перейти к адресу a.
        GOTO <a>  - перейти к адресу a
        RETURN    - завершить работу
    """
    LOAD, STORE, CONST, POP, ADD, SUB, LT, JZ, JNZ, GOTO, RETURN = range(11)

    to_str = {LOAD: 'load',
              STORE: 'store',
              CONST: 'const',
              POP: 'pop',
              ADD: 'add',
              SUB: 'sub',
              LT: 'lt',
              JZ: 'jz',
              JNZ: 'jnz',
              GOTO: 'goto',
              RETURN: 'return'}
