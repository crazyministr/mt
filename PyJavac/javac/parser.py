# -*- coding: utf-8 -*-
import sys
from javac.lexer import Lexer


class Node:
    def __init__(self, kind, value=None, op1=None, op2=None, op3=None):
        self.kind = kind
        self.value = value
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3


class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.source_code = None
        self.parse_position = 0
        self.current_char = ' '
        self.token_type = None
        self.value = None

    def error(self, msg):
        print 'Parser error:', msg
        sys.exit(1)

    def term(self):
        if self.token_type == Lexer.VAR:
            n = Node(Lexer.VAR, self.value)
            self.next_token()
            return n
        elif self.token_type == Lexer.INT:
            n = Node(Lexer.INT, self.value)
            self.next_token()
            return n
        else:
            return self.brackets_expression()

    def add(self):
        n = self.term()
        while self.token_type == Lexer.PLUS or self.token_type == Lexer.MINUS:
            if self.token_type == Lexer.PLUS:
                kind = Lexer.PLUS
            else:
                kind = Lexer.MINUS
            self.next_token()
            n = Node(kind, op1=n, op2=self.term())
        return n

    def test(self):
        n = self.add()
        if self.token_type == Lexer.LESS:
            self.next_token()
            n = Node(Lexer.LESS, op1=n, op2=self.add())
        if self.token_type == Lexer.GREAT:
            self.next_token()
            n = Node(Lexer.GREAT, op1=n, op2=self.add())
        return n

    def expression(self):
        if self.token_type != Lexer.VAR:
            return self.test()
        n = self.test()
        if n.kind == Lexer.VAR and self.token_type == Lexer.EQUAL:
            self.next_token()
            n = Node(Lexer.EQUAL, op1=n, op2=self.expression())
        return n

    def brackets_expression(self):
        if self.token_type != Lexer.LPAR:
            self.error('"(" expected')
        self.next_token()
        n = self.expression()
        if self.token_type != Lexer.RPAR:
            self.error('")" expected')
        self.next_token()
        return n

    def statement(self):
        if self.token_type == Lexer.IF:
            n = Node(Lexer.IF)
            self.next_token()
            n.op1 = self.brackets_expression()
            n.op2 = self.statement()
            if self.token_type == Lexer.ELSE:
                n.kind = Lexer.ELSE
                self.next_token()
                n.op3 = self.statement()
        elif self.token_type == Lexer.WHILE:
            n = Node(Lexer.WHILE)
            self.next_token()
            n.op1 = self.brackets_expression()
            n.op2 = self.statement()
        elif self.token_type == Lexer.DO:
            n = Node(Lexer.DO)
            self.next_token()
            n.op1 = self.statement()
            if self.token_type != Lexer.WHILE:
                self.error('"while" expected')
            self.next_token()
            n.op2 = self.brackets_expression()
            if self.token_type != Lexer.SEMICOLON:
                self.error('";" expected')
        elif self.token_type == Lexer.SEMICOLON:
            n = Node(Lexer.EMPTY)
            self.next_token()
        elif self.token_type == Lexer.LBRA:
            n = Node(Lexer.EMPTY)
            self.next_token()
            while self.token_type != Lexer.RBRA:
                n = Node(Lexer.RBRA, op1=n, op2=self.statement())
            self.next_token()
        else:
            n = Node(Lexer.EXPR, op1=self.expression())
            if self.token_type != Lexer.SEMICOLON:
                self.error('";" expected')
            self.next_token()
        return n

    def next_char(self):
        if self.parse_position == len(self.source_code):
            self.current_char = ''
            return

        self.current_char = self.source_code[self.parse_position]
        self.parse_position += 1

    def next_token(self):
        self.value = None
        self.token_type = None
        while self.token_type is None:
            if len(self.current_char) == 0:  # end of code
                self.token_type = Lexer.EOF
            elif self.current_char.isspace() or self.current_char == '\n':  # space or \n
                self.next_char()
            elif self.current_char in Lexer.SYMBOLS:  # if it's from Lexer.SYMBOLS
                self.token_type = Lexer.SYMBOLS[self.current_char]
                self.next_char()
            elif self.current_char.isdigit():  # a number
                int_val = 0
                while self.current_char.isdigit():
                    int_val = int_val * 10 + int(self.current_char)
                    self.next_char()
                self.value = int_val
                self.token_type = Lexer.INT
            elif self.current_char.isalpha():  # a word/variable
                variable = ''
                while self.current_char.isalpha() or self.current_char.isdigit():
                    variable += self.current_char
                    self.next_char()
                if variable in Lexer.WORDS:
                    self.token_type = Lexer.WORDS[variable]
                else:
                    self.token_type = Lexer.VAR
                    self.value = variable
            else:
                self.error('Unexpected token: ' + self.current_char)

    def parse(self, source_code):
        self.source_code = source_code
        self.next_token()
        node = Node(Lexer.EOF, op1=self.statement())
        return node
