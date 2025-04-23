import math

def evalu(node):
    match node:
        case ['int', value]:
            return int(value)

        case ['float', value]:
            return float(value)

        case ['binop', op, left, right]:
            match op:
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
                    return evalu(left) & evalu(right)
                case 'or':
                    return evalu(left) | evalu(right)
                case 'xor':
                    return evalu(left) ^ evalu(right)
                case 'mod':
                    return evalu(left) % evalu(right)

        case ['binop_two', _, left, right]:
            return evalu(left) ** evalu(right)

        case ['post_unop', _, operand]:
            return evalu(operand)

        case ['post_unop_two', op, operand]:
            match op:
                case '++':
                    return evalu(operand) + 1
                case '--':
                    return evalu(operand) - 1

        case ['pre_unop', op, operand]:
            match op:
                case '+':
                    return evalu(operand)
                case '-':
                    return -evalu(operand)
