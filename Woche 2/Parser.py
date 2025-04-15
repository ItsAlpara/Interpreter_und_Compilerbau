from ply.yacc import yacc





def p_number(p):
    'expression : NUMBER'
    p[0] = ('int',p[1])


#def p_plus(p):
#    'expression : PLUS expression'
#    p[0] = ('binop','PLUS',p[1] + p[3])
#
#def p_minus(p):
#    'expression : PLUS expression'
#    p[0] = ('binop','MINUS',p[1] + p[3])

#def p_times(p):
#    'expression : PLUS expression'
#    p[0] = ('binop','TIMES',p[1] + p[3])

#def p_divide(p):
#    'expression : PLUS expression'
#    p[0] = ('binop','DIVIDE',p[1] + p[3])

def p_binop(p):
    'expression : PLUS expression'
    p[0] = ('binop', '', p[1] + p[3])