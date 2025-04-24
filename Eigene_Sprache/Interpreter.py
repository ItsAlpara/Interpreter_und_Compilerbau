import math

state = {"x": 1,"y":0,"z":0}

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
                    return evalu(left) <= evalu(right)

                case '>=':
                    return evalu(left) >= evalu(right)

                case '<':
                    return evalu(left) < evalu(right)

                case '>':
                    return evalu(left) > evalu(right)

                case '=':
                    return evalu(left) == evalu(right)

                case '!=':
                    return evalu(left) != evalu(right)

                case 'and':
                    return min(evalu(left), evalu(right))

                case 'or':
                    return max(evalu(left), evalu(right))

                case 'xor':
                    el = evalu(left)
                    er = evalu(right)
                    if el != 0 and er != 0:
                        return 0
                    else:
                        el ^ er

                case 'mod':
                    return evalu(left) % evalu(right)

###Hier noch Komplexe Zahlen einfügen und Emojis

        case ['binop_two', _, left, right]:
            return evalu(left) ** evalu(right)

        case ['post_unop', _, operand]:
            return evalu(operand)

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
