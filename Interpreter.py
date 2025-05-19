import math

def evalu(node, state):
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
                    er = evalu(right, state)
                case ':=:=':
                    er = evalu(right, state)
                case '+:=':
                    er = evalu(('binop','+',left,right), state)
                case '-:=':
                    er = evalu(('binop','-',left,right), state)
                case '*:=':
                    er = evalu(('binop','*',left,right), state)
                case '|:=':
                    er = evalu(('binop','|',left,right), state)
                case '/:=':
                    er = evalu(('binop','/',left,right), state)
                case '\\:=':
                    er = evalu(('binop','\\',left,right), state)
                case 'mod:=':
                    er = evalu(('binop','mod',left,right), state)
                case '**:=':
                    er = evalu(('binop_two','**',left,right), state)
                case 'E:=':
                    er = evalu(('binop','E',left,right), state)
                case '<:=':
                    er = evalu(('binop','<',left,right), state)
                case '>:=':
                    er = evalu(('binop','>',left,right), state)
                case '<=:=':
                    er = evalu(('binop','<=',left,right), state)
                case '>=:=':
                    er = evalu(('binop','>=',left,right), state)
                case '=:=':
                    er = evalu(('binop','=',left,right), state)
                case '!=:=':
                    er = evalu(('binop','!=',left,right), state)
                case 'or:=':
                    er = evalu(('binop','or',left,right), state)
                case 'xor:=':
                    er = evalu(('binop','xor',left,right), state)
                case 'and:=':
                    er = evalu(('binop','and',left,right), state)
            state[left[1]] = er
            return state[left[1]]

        case ['comp_seq', seq]:
            i = len(seq)
            last_eval = evalu(seq[0], state)
            value = True
            temp_value = True
            for x in range(0,i//2):
                temp_eval = evalu(seq[2*(x+1)], state)
                match seq[2*x+1]:
                    case '<=':
                        temp_value = last_eval <= temp_eval
                    case '>=':
                        temp_value = last_eval >= temp_eval 
                    case '<':
                        temp_value = last_eval < temp_eval 
                    case '>':
                        temp_value = last_eval > temp_eval 
                    case '=':
                        temp_value = last_eval == temp_eval 
                    case '!=':
                        temp_value = last_eval != temp_eval
                value = value and temp_value
                last_eval = temp_eval
            return int(value)


        case ['binop', op, left, right]:
            el = evalu(left, state)
            er = evalu(right, state)
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
            el = evalu(left, state)
            er = evalu(right, state)
            match(op):
                case('**'):
                    return el ** er


        case ['post_unop', 'imag', operand]:
            return complex(0,operand[1])

        case ['pre_unop', op, operand]:
            match op:
                case '+':
                    return abs(evalu(operand, state))
                case '-':
                    return -evalu(operand, state)
                case 'not':
                    return 0 if evalu(operand, state) != 0 else 1

######SEQ
        case['sequence_body',value]:
            return evalu(value, state)

        case['ex_sem_seq',left,right]:
            evalu(left, state)
            return evalu(right, state)

        case['ex_sem',value]:
            return evalu(value, state)

##############

        case['if',cond,expr]:
            return evalu(expr, state) if evalu(cond, state) else None
            
        case['if_else',cond,expr1,expr2]:
            return evalu(expr1, state) if evalu(cond, state) else evalu(expr2, state)

        case['while',cond,expr]:
            ret = None
            while(evalu(cond, state)):
                ret = evalu(expr, state)
            return ret

        case['loop',ident,brack1,lexpr,rexpr,brack2,expr]:
            lexpr_eval = evalu(lexpr, state)
            rexpr_eval = evalu(rexpr, state)
            ret = None
            low = lexpr_eval if brack1[1] == '[' else lexpr_eval + 1
            high = rexpr_eval if brack1[1] == '[' else rexpr_eval + 1
            i = low
            for _ in range(low, high):
                state[ident[1]] = i
                i = i + 1
                ret = evalu(expr, state)
            return ret
