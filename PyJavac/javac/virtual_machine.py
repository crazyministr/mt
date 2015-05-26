# -*- coding: utf-8 -*-
class VirtualMachine:
    def __init__(self, file_name):
        self.instructions = self._parse_instructions(file_name)

    def run(self):
        var = [0 for i in xrange(26)]
        stack = []
        addr = 0
        step = 0
        while True:
            step += 1
            if step == 100:
                break

            instruction = self.instructions[addr]
            addr += 1

            operation = instruction.split('_')
            if instruction.find(' ') > -1:
                operation = instruction.split(' ')

            op = operation[0]
            if len(operation) > 1:
                arg = int(operation[1])

            if op == 'load':
                stack.append(var[arg])
            elif op == 'store':
                var[arg] = stack[-1]
            elif op == 'const':
                stack.append(arg)
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
            elif op == 'jz':
                if stack.pop() == 0:
                    addr = arg
            elif op == 'jnz':
                if stack.pop() != 0:
                    addr = arg
            elif op == 'goto':
                addr = arg
            elif op == 'return':
                break

        print 'Execution finished.'
        for i in xrange(26):
            if var[i] != 0:
                print '%c = %d' % (chr(i + ord('a')), var[i])

    def _parse_instructions(self, file_name):
        _file = open(file_name, 'r')
        instructions = []
        for inst in _file:
            if inst != '':
                instructions.append(inst[inst.find(': ') + 2:])
                if instructions[-1][-1] == '\n':
                    instructions[-1] = instructions[-1][:-1]

        return instructions
