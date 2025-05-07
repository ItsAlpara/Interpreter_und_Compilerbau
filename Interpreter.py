import math

state = {"x": 0,"y":0,"z":0}

def evalu(node):
    match node:
        case ['identifier',value]:
            return state[value]

        case ['int', value]:
            return int(value)

        case ['float', value]:
            return float(value)

        case ['assign', op, left, right]:
            er = 0
            match op:
                case ':=':
                    er = evalu(right)
                case ':=:=':
                    er = evalu(right)
                case '+:=':
                    er = evalu(('binop','+',left,right))
                case '-:=':
                    er = evalu(('binop','-',left,right))
                case '*:=':
                    er = evalu(('binop','*',left,right))
                case '|:=':
                    er = evalu(('binop','|',left,right))
                case '/:=':
                    er = evalu(('binop','/',left,right))
                case '\\:=':
                    er = evalu(('binop','\\',left,right))
                case 'mod:=':
                    er = evalu(('binop','mod',left,right))
                case '**:=':
                    er = evalu(('binop_two','**',left,right))
                case 'E:=':
                    er = evalu(('binop','E',left,right))
                case '<:=':
                    er = evalu(('binop','<',left,right))
                case '>:=':
                    er = evalu(('binop','>',left,right))
                case '<=:=':
                    er = evalu(('binop','<=',left,right))
                case '>=:=':
                    er = evalu(('binop','>=',left,right))
                case '=:=':
                    er = evalu(('binop','=',left,right))
                case '!=:=':
                    er = evalu(('binop','!=',left,right))
                case 'or:=':
                    er = evalu(('binop','or',left,right))
                case 'xor:=':
                    er = evalu(('binop','xor',left,right))
                case 'and:=':
                    er = evalu(('binop','and',left,right))
            state[left[1]] = er
            return state[left[1]]

        case ['binop', op, left, right]:
            el = evalu(left)
            er = evalu(right)
            match op:
                case '+':
                    return el + er

                case '-':
                    return el - er

                case '*':
                    return el * er

                case '|':
                    return el / er

                case '/':
                    return math.ceil(el / er)

                case '\\':
                    return math.floor(el / er)

                case '<=':
                    return int(el <= er)

                case '>=':
                    return int(el >= er)

                case '<':
                    return int(el < er)

                case '>':
                    return int(el > er)

                case '=':
                    return int(el == er)

                case '!=':
                    return int(el != er)

                case 'and':
                    if el == 0 or er == 0:
                        return 0
                    else:
                        return 1

                case 'or':
                    if el != 0 and er != 0:
                        return 1
                    else:
                        return 0

                case 'xor':
                    if (el != 0 and er != 0) or (el == 0 and er == 0):
                        return 0
                    else:
                        return 1

                case 'mod':
                    return el % er

                case 'E':
                    return el * (10**er)  # Angepasst E als OP

        case ['binop_two', op, left, right]:
            el = evalu(left)
            er = evalu(right)
            match(op):
                case('**'):
                    return el ** er


        case ['post_unop', 'imag', operand]:
            return complex(0,operand[1])


        case ['post_unop_two', op, operand]:
            match op:
                case '++':
                    if operand[0] == 'identifier':
                        state[operand[1]] += 1
                        return state[operand[1]]
                    else:
                        return evalu(operand) + 1
                case '--':
                    if operand[0] == 'identifier':
                        state[operand[1]] -= 1
                        return state[operand[1]]
                    else:
                        return evalu(operand) - 1

        case ['pre_unop', op, operand]:
            match op:
                case '+':
                    return abs(evalu(operand))
                case '-':
                    return -evalu(operand)
                case 'not':
                    return 0 if evalu(operand) != 0 else 1

######SEQ
        case['sequence_body',value]:
            return evalu(value)

        case['ex_sem_seq',left,right]:
            evalu(left)
            return evalu(right)

        case['ex_sem',value]:
            return evalu(value)
