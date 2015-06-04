# -*- coding: utf-8 -*-
import sys


class Lexer(object):
    INT, VAR, IF, ELSE, WHILE, DO, LBRA, RBRA, LPAR, RPAR, PLUS, MINUS, MUL, DIV, LESS, GREAT, \
        EXPR, EQUAL, SEMICOLON, EMPTY, EOF = range(21)

    SYMBOLS = {'{': LBRA, '}': RBRA,
               '=': EQUAL,
               ';': SEMICOLON,
               '(': LPAR, ')': RPAR,
               '+': PLUS, '-': MINUS, '*': MUL, '/': DIV,
               '<': LESS, '>': GREAT}

    WORDS = {'if': IF, 'else': ELSE, 'do': DO, 'while': WHILE}

    @staticmethod
    def error(msg):
        print 'Lexer error: ', msg
        sys.exit(1)
