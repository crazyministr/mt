# -*- coding: utf-8 -*-
from javac.jvm_insructions import *
from javac.parser import Parser
from javac.lexer import Lexer


class Compiler:
    jvm_instructions = []
    addr = 0

    def __init__(self):
        self.parser = Parser()

    def add_command(self, instruction, variable=None, addr=None):
        word = JVMInstructions.to_str[instruction]
        if variable is None:
            self.jvm_instructions.append(word + ('' if addr is None else ' ' + str(addr)))
        else:
            self.jvm_instructions.append(word + '_' + str(variable))
        self.addr += 1

    def _compile(self, node):
        if node.kind == Lexer.VAR:
            self.add_command(JVMInstructions.LOAD, node.value)
        elif node.kind == Lexer.INT:
            self.add_command(JVMInstructions.CONST, node.value)
        elif node.kind == Lexer.PLUS:
            self._compile(node.op1)
            self._compile(node.op2)
            self.add_command(JVMInstructions.ADD)
        elif node.kind == Lexer.MINUS:
            self._compile(node.op1)
            self._compile(node.op2)
            self.add_command(JVMInstructions.SUB)
        elif node.kind == Lexer.LESS:
            self._compile(node.op1)
            self._compile(node.op2)
            self.add_command(JVMInstructions.LT)
        elif node.kind == Lexer.GREAT:
            self._compile(node.op1)
            self._compile(node.op2)
            self.add_command(JVMInstructions.GT)
        elif node.kind == Lexer.EQUAL:
            self._compile(node.op2)
            self.add_command(JVMInstructions.STORE, node.op1.value)
        elif node.kind == Lexer.IF:
            self._compile(node.op1)
            addr = self.addr
            self.add_command(JVMInstructions.JZ, addr=0)
            self._compile(node.op2)
            self.jvm_instructions[addr] = self.jvm_instructions[addr][:-1] + str(self.addr)
        elif node.kind == Lexer.ELSE:
            self._compile(node.op1)
            addr1 = self.addr
            self.add_command(JVMInstructions.JZ, addr=0)
            self._compile(node.op2)
            addr2 = self.addr
            self.add_command(JVMInstructions.GOTO, addr=0)
            self.jvm_instructions[addr1] = self.jvm_instructions[addr1][:-1] + str(self.addr)
            self._compile(node.op3)
            self.jvm_instructions[addr2] = self.jvm_instructions[addr2][:-1] + str(self.addr)
        elif node.kind == Lexer.WHILE:
            addr1 = self.addr
            self._compile(node.op1)
            addr2 = self.addr
            self.add_command(JVMInstructions.JZ, addr=0)
            self._compile(node.op2)
            self.add_command(JVMInstructions.GOTO, addr=addr1)
            self.jvm_instructions[addr2] = self.jvm_instructions[addr2][:-1] + str(self.addr)
        elif node.kind == Lexer.DO:
            addr = self.addr
            self._compile(node.op1)
            self._compile(node.op2)
            self.add_command(JVMInstructions.JNZ, addr=addr)
        elif node.kind == Lexer.RBRA:
            self._compile(node.op1)
            self._compile(node.op2)
        elif node.kind == Lexer.EXPR:
            self._compile(node.op1)
            self.add_command(JVMInstructions.POP)
        elif node.kind == Lexer.EOF:
            self._compile(node.op1)
            self.add_command(JVMInstructions.RETURN)

        return self.jvm_instructions

    def compile(self, file_name):
        _file = open(file_name, 'r')
        ast = self.parser.parse(_file.read())
        return self._compile(ast)
