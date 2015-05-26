# -*- coding: utf-8 -*-
import sys


class Lexer(object):
    NUM, ID, IF, ELSE, WHILE, DO, LBRA, RBRA, LPAR, RPAR, PLUS, MINUS, LESS, \
        EQUAL, SEMICOLON, EOF = range(16)

    SYMBOLS = {'{': LBRA, '}': RBRA,
               '=': EQUAL,
               ';': SEMICOLON,
               '(': LPAR, ')': RPAR,
               '+': PLUS, '-': MINUS,
               '<': LESS}

    WORDS = {'if': IF, 'else': ELSE, 'do': DO, 'while': WHILE}

    @staticmethod
    def error(msg):
        print 'Lexer error: ', msg
        sys.exit(1)
