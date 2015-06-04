# -*- coding: utf-8 -*-


class VirtualMachine:
    def __init__(self, file_name):
        self.instructions = self._parse_instructions(file_name)

    def run(self):
        variables = {}
        stack = []
        addr = 0
        while True:
            instruction = self.instructions[addr]
            addr += 1

            operation = instruction.split('_')
            if instruction.find(' ') > -1:
                operation = instruction.split(' ')

            arg = ''
            op = operation[0]
            if len(operation) > 1:
                arg = operation[1]

            if op == 'load':
                stack.append(variables[arg])
            elif op == 'store':
                variables[arg] = stack[-1]
            elif op == 'const':
                stack.append(int(arg))
            elif op == 'pop':
                stack.pop()
            elif op == 'add':
                stack[-2] += stack[-1]
                stack.pop()
            elif op == 'sub':
                stack[-2] -= stack[-1]
                stack.pop()
            elif op == 'lt':
                if stack[-2] < stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
            elif op == 'gt':
                if stack[-2] > stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
            elif op == 'jz':
                if stack.pop() == 0:
                    addr = int(arg)
            elif op == 'jnz':
                if stack.pop() != 0:
                    addr = int(arg)
            elif op == 'goto':
                addr = int(arg)
            elif op == 'return':
                break

        print 'Variables:'
        for k, v in variables.items():
            print k, '=', v

    def _parse_instructions(self, file_name):
        _file = open(file_name, 'r')
        instructions = []
        for inst in _file:
            if inst != '':
                instructions.append(inst[inst.find(': ') + 2:])
                if instructions[-1][-1] == '\n':
                    instructions[-1] = instructions[-1][:-1]

        return instructions
