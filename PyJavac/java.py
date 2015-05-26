# -*- coding: utf-8 -*-
import sys
from javac.virtual_machine import VirtualMachine


def main():
    # file_name = sys.argv[1]
    file_name = 'example.class'

    vm = VirtualMachine(file_name)
    vm.run()

main()
