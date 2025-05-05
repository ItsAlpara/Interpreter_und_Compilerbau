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

        case ['binop', op, left, right]:
            match op:
                case ':=':
                    state[left[1]] = evalu(right)
                    return state[left[1]]

                case '+':
                    return evalu(left) + evalu(right)

                case '-':
                    return evalu(left) - evalu(right)

                case '*':
                    return evalu(left) * evalu(right)

                case '|':
                    return evalu(left) / evalu(right)

                case '/':
                    return math.ceil(evalu(left) / evalu(right))

                case '\\':
                    return math.floor(evalu(left) / evalu(right))

                case '<=':
                    return int(evalu(left) <= evalu(right))

                case '>=':
                    return int(evalu(left) >= evalu(right))

                case '<':
                    return int(evalu(left) < evalu(right))

                case '>':
                    return int(evalu(left) > evalu(right))

                case '=':
                    return int(evalu(left) == evalu(right))

                case '!=':
                    return int(evalu(left) != evalu(right))

                case 'and':
                    if evalu(left) == 0 | evalu(right) == 0:
                        return 0
                    else:
                        return 1

                case 'or':
                    if evalu(left) != 0 & evalu(right) != 0:
                        return 1
                    else:
                        return 0

                case 'xor':
                    el = evalu(left)
                    er = evalu(right)
                    if (el != 0 and er != 0) | (el == 0 and er == 0):
                        return 0
                    else:
                        return 1

                case 'mod':
                    return evalu(left) % evalu(right)

                case 'E':
                    return evalu(left) * (10**evalu(right))  # Angepasst E als OP

        case ['binop_two', op, left, right]:
            match(op):
                case('**'):
                    return evalu(left) ** evalu(right)


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