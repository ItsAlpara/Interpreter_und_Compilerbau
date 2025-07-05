import math
from Entry import *

def evalu(node, env):
    match node:
        case ['identifier',value]:
            return env[value].value
        case ['int', value]:
            return int(value)
        case ['float', value]:
            return float(value)
        case ['string', value]:
            return str(value[1:-1])
        case ['assign', op, left, right]:
            er = 0
            match op:
                case ':=':
                    er = evalu(right, env)
                case ':=:=':
                    er = evalu(right, env)
                case '+:=':
                    er = evalu(('binop','+',left,right), env)
                case '-:=':
                    er = evalu(('binop','-',left,right), env)
                case '*:=':
                    er = evalu(('binop','*',left,right), env)
                case '|:=':
                    er = evalu(('binop','|',left,right), env)
                case '/:=':
                    er = evalu(('binop','/',left,right), env)
                case '\\:=':
                    er = evalu(('binop','\\',left,right), env)
                case 'mod:=':
                    er = evalu(('binop','mod',left,right), env)
                case '**:=':
                    er = evalu(('binop_two','**',left,right), env)
                case 'E:=':
                    er = evalu(('binop','E',left,right), env)
                case '<:=':
                    er = evalu(('binop','<',left,right), env)
                case '>:=':
                    er = evalu(('binop','>',left,right), env)
                case '<=:=':
                    er = evalu(('binop','<=',left,right), env)
                case '>=:=':
                    er = evalu(('binop','>=',left,right), env)
                case '=:=':
                    er = evalu(('binop','=',left,right), env)
                case '!=:=':
                    er = evalu(('binop','!=',left,right), env)
                case 'or:=':
                    er = evalu(('binop','or',left,right), env)
                case 'xor:=':
                    er = evalu(('binop','xor',left,right), env)
                case 'and:=':
                    er = evalu(('binop','and',left,right), env)
            env[left[1]].value = er
            return er

        case ['comp_seq', seq]:
            i = len(seq)
            last_eval = evalu(seq[0], env)
            value = True
            temp_value = True
            for x in range(0,i//2):
                temp_eval = evalu(seq[2*(x+1)], env)
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
            el = evalu(left, env)
            er = evalu(right, env)
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
            el = evalu(left, env)
            er = evalu(right, env)
            match(op):
                case('**'):
                    return el ** er


        case ['post_unop', 'imag', operand]:
            return complex(0,operand[1])

        case ['pre_unop', op, operand]:
            match op:
                case '+':
                    return abs(evalu(operand, env))
                case '-':
                    return -evalu(operand, env)
                case 'not':
                    return 0 if evalu(operand, env) != 0 else 1

######SEQ
        case['sequence_body',value]:
            return evalu(value, env)

        case['ex_sem_seq',left,right]:
            evalu(left, env)
            return evalu(right, env)

        case['ex_sem',value]:
            return evalu(value, env)

#### LAMBDA ##############
        case['ex_lambda',params,expr]:
            return (env,params,expr)

#### CALL ################
        case ['ex_call', function, params]:

            (env_f,params_f,expr_f) = evalu(function, env)

            paramlist = []
            oversupplyvar = None
            env_new = SymbolTable(parent=env_f)
            new_params = ['paramlist']

            for param in params_f[1]:
                paramlist.append(param[1])
            if params_f[0] == 'paramlist_point':
                oversupplyvar = params_f[2][1]
                env_new.put(oversupplyvar)
                env_new[oversupplyvar].value = []
                new_params = ['paramlist_point']

            for param in params:
                if param[0] == 'callparam_assignment':
                    if param[1][1] in paramlist:
                        val = evalu(param[2], env)
                        env_new.put(param[1][1])
                        env_new[param[1][1]].value = val
                        paramlist.remove(param[1][1])
            for param in params:
                if param[0] == 'callparam_expr':
                    val = evalu(param[1], env)
                    try:
                        p = paramlist.pop(0)
                        env_new.put(p)
                        env_new[p].value = val
                    except IndexError:
                        if oversupplyvar is not None:
                            env_new[oversupplyvar].value.append(val)
                        else:
                            print('error: oversupply variable not found')
            if paramlist:
                templist = []
                for param in paramlist:
                    templist.append(('identifier',param))
                new_params.append(tuple(templist))
                return (env_new,tuple(new_params),expr_f)
            return evalu(expr_f, env_new)

############## LISTS ############################
        case['arr',elements]:
            ele = []
            for element in elements:
                ele.append(evalu(element, env))
            return ele

        case['list',val]:
            def make_list(val):
                (car,cdr) = val
                if cdr == None:
                    return (evalu(car,env),None)
                return (evalu(car,env),make_list(cdr))
            return make_list(val)

        case['cons',val1,val2]:
            eval1 = evalu(val1,env)
            eval2 = evalu(val2,env)
            return (eval1,eval2)
            
        case None:
            return None

        case['list_get',lis,index]:
            val = evalu(lis,env)
            idx = evalu(index,env)
            if type(val)==list:
                return val[idx]
            if type(val)==tuple:
                def get_list(l,i):
                    (car,cdr) = l
                    if i == 0:
                        return car
                    return get_list(cdr,i-1)
                return get_list(val,idx)

        case['rest_list_get',lis]:
            val = evalu(lis,env)
            if val == None:
                return None
            if type(val) == list:
                return val[1:]
            if type(val) == tuple:
                (car,cdr) = val
                return cdr
                
        case['list_len',lis]:
            val = evalu(lis,env)
            if val == None:
                return 0
            if type(val) == list:
                return len(evalu(lis, env))
            if type(val) == tuple:
                def get_len(l):
                    (car,cdr) = l
                    if cdr == None:
                        return 1
                    return get_len(cdr) + 1
                return get_len(val)


############## CONTROL STRUCTS ###################

        case['if',cond,expr]:
            return evalu(expr, env) if evalu(cond, env) else None
            
        case['if_else',cond,expr1,expr2]:
            return evalu(expr1, env) if evalu(cond, env) else evalu(expr2, env)

        case['while',cond,expr]:
            ret = None
            while(evalu(cond, env)):
                ret = evalu(expr, env)
            return ret

        case['loop',ident,lexpr,expr]:
            env_new = env.push(ident[1])
            lexpr_eval = evalu(lexpr, env)
            ret = None
            if lexpr_eval == None:
                return ret
            if type(lexpr_eval) == list:
                for i in lexpr_eval:
                    env_new[ident[1]].value = i
                    ret = evalu(expr, env_new)
                return ret
            if type(lexpr_eval) == tuple:
                def get_len(l):
                    (car,cdr) = l
                    if cdr == None:
                        return 1
                    return get_len(cdr) + 1
                list_len = get_len(lexpr_eval)
                i = lexpr_eval
                for _ in range(0,list_len):
                    env_new[ident[1]].value = i
                    ret = evalu(expr,env_new)
                    (car,cdr) = i
                    i = cdr
                return ret

        case['pointloop',ident,low,high,expr]:
            env_new = env.push(ident[1])
            ret = None
            loweval = evalu(low,env)
            higheval = evalu(high,env)
            for i in range(loweval,higheval+1):
                env_new[ident[1]].value = i
                ret = evalu(expr, env_new)
            return ret

################## LET
        case['exp_let',letlist,body]:
            identlist = [name[1] for name, _ in letlist]
            env_new = env.push(identlist)
            for (name, expr) in letlist:
                value = evalu(expr, env_new)
                env_new[name[1]].value = value
            return evalu(body, env_new)

################## STRUCTS
        case['struct',idexprlist]:
            struct=[]
            for ele in idexprlist:
                struct.append((ele[0][1],evalu(ele[1],env)))
            return struct

        case['structaccess',structexpr,ident]:
            struct = evalu(structexpr,env)
            for ele in struct:
                if ele[0]==ident[1]:
                    return ele[1]
            return None

################## MISC
        case['echo',expr]:
            val = evalu(expr, env)
            print(val)
            return val

    return None
