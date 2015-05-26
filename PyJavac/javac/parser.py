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
    VAR, CONST, ADD, SUB, LT, SET, IF1, IF2, WHILE, DO, EMPTY, SEQ, EXPR, PROGRAM = range(14)

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
        if self.token_type == Lexer.ID:
            n = Node(Parser.VAR, self.value)
            self.next_token()
            return n
        elif self.token_type == Lexer.NUM:
            n = Node(Parser.CONST, self.value)
            self.next_token()
            return n
        else:
            return self.paren_expr()

    def add(self):
        n = self.term()
        while self.token_type == Lexer.PLUS or self.token_type == Lexer.MINUS:
            if self.token_type == Lexer.PLUS:
                kind = Parser.ADD
            else:
                kind = Parser.SUB
            self.next_token()
            n = Node(kind, op1=n, op2=self.term())
        return n

    def test(self):
        n = self.add()
        if self.token_type == Lexer.LESS:
            self.next_token()
            n = Node(Parser.LT, op1=n, op2=self.add())
        return n

    def expr(self):
        if self.token_type != Lexer.ID:
            return self.test()
        n = self.test()
        if n.kind == Parser.VAR and self.token_type == Lexer.EQUAL:
            self.next_token()
            n = Node(Parser.SET, op1=n, op2=self.expr())
        return n

    def paren_expr(self):
        if self.token_type != Lexer.LPAR:
            self.error('"(" expected')
        self.next_token()
        n = self.expr()
        if self.token_type != Lexer.RPAR:
            self.error('")" expected')
        self.next_token()
        return n

    def statement(self):
        if self.token_type == Lexer.IF:
            n = Node(Parser.IF1)
            self.next_token()
            n.op1 = self.paren_expr()
            n.op2 = self.statement()
            if self.token_type == Lexer.ELSE:
                n.kind = Parser.IF2
                self.next_token()
                n.op3 = self.statement()
        elif self.token_type == Lexer.WHILE:
            n = Node(Parser.WHILE)
            self.next_token()
            n.op1 = self.paren_expr()
            n.op2 = self.statement()
        elif self.token_type == Lexer.DO:
            n = Node(Parser.DO)
            self.next_token()
            n.op1 = self.statement()
            if self.token_type != Lexer.WHILE:
                self.error('"while" expected')
            self.next_token()
            n.op2 = self.paren_expr()
            if self.token_type != Lexer.SEMICOLON:
                self.error('";" expected')
        elif self.token_type == Lexer.SEMICOLON:
            n = Node(Parser.EMPTY)
            self.next_token()
        elif self.token_type == Lexer.LBRA:
            n = Node(Parser.EMPTY)
            self.next_token()
            while self.token_type != Lexer.RBRA:
                n = Node(Parser.SEQ, op1=n, op2=self.statement())
            self.next_token()
        else:
            n = Node(Parser.EXPR, op1=self.expr())
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
            if len(self.current_char) == 0:
                self.token_type = Lexer.EOF
            elif self.current_char.isspace() or self.current_char == '\n':
                self.next_char()
            elif self.current_char in Lexer.SYMBOLS:
                self.token_type = Lexer.SYMBOLS[self.current_char]
                self.next_char()
            elif self.current_char.isdigit():
                intval = 0
                while self.current_char.isdigit():
                    intval = intval * 10 + int(self.current_char)
                    self.next_char()
                self.value = intval
                self.token_type = Lexer.NUM
            elif self.current_char.isalpha():
                ident = ''
                while self.current_char.isalpha():
                    ident += self.current_char.lower()
                    self.next_char()
                if ident in Lexer.WORDS:
                    self.token_type = Lexer.WORDS[ident]
                elif len(ident) == 1:
                    self.token_type = Lexer.ID
                    self.value = ord(ident) - ord('a')
                else:
                    self.error('Unknown identifier: ' + ident)
            else:
                self.error('Unexpected token_typebol: ' + self.current_char)

    def parse(self, source_code):
        self.source_code = source_code
        self.next_token()
        node = Node(Parser.PROGRAM, op1=self.statement())
        if self.token_type != Lexer.EOF:
            self.lexer.error("Invalid statement syntax")
        return node
