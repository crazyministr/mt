# -*- coding: utf-8 -*-
import sys
from javac.compiler import Compiler


def main():
    file_name = sys.argv[1]
    # file_name = "example.java"

    compiler = Compiler()
    jvm_instructions = compiler.compile(file_name)

    result_file = open(file_name.replace('.java', '.class'), "w")
    result_file.write('\n'.join(str('%3d: ' % i) + inst for i, inst in enumerate(jvm_instructions)))
    result_file.close()

main()
