import math
from math import floor

def eval(node):
    if node[0] == 'int':
        return int(node[1])

    if node[0] == 'float':
        return float(node[1])

    if node[0] == 'binop':
        op = node[1]
        left = eval(node[2])
        right = eval(node[3])
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '|':
            return left / right
        elif op == '/':
            return math.ceil(left / right)
        elif op == '\\':
            return floor(left / right)
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '=':
            return left == right
        elif op == '!=':
            return left != right
        elif op == 'and':
            return left & right
        elif op == 'or':
            return left | right
        elif op == 'xor':
            return left ^ right
        elif op == 'mod':
            return left % right

    ##POWER##
    if node[0] == 'binop_two':
        return eval(node[2])**eval(node[3])

    ##IMAGINARY##
    if node[0] == 'post_unop':
        return eval(node[2])

    ###POST_INC_DEC###
    if node[0] == 'post_unop_two':
        if node[1] == '++':
            return eval(node[2])+1
        elif node[1] == '--':
            return eval(node[2])-1

    ###PRE###
    if node[0] == 'pre_unop':
        if node[1] == '+':
            return eval(node[2])
        elif node[1] == '-':
            return -eval(node[2])

    if node[0] == "Syntax error in input!":
        print("Syntax error in input!")
