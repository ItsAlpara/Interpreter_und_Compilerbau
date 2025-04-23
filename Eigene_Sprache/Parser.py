from Lexer import tokens
from ply.yacc import yacc

start = 'expression'

precedence = (
    ('nonassoc','EX_CAST'),
    ('nonassoc','ASS_EX_CAST'),
    ('right','ASSIGN'),
    ('nonassoc','BIN_EX_CAST'),
    ('left','OR'),
    ('left','XOR'),
    ('left','AND'),
    ('left','EQUAL','NOT_EQUAL'),
    ('nonassoc','GREATER_THAN','LESS_THAN','GREATER_EQUAL','LESS_EQUAL'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','CEIL_DIVIDE','FLOOR_DIVIDE','MODULO'),
    ('left','POWER'),
    ('nonassoc','UN_EX_CAST'),
    ('right','PRE_PLUS','PRE_MINUS'),
    ('nonassoc','TWO_UN_EX_CAST'),
#    ('right','PRE_INCR','PRE_DECR'),
    ('nonassoc','POST_EX_CAST'),
    ('left','IMAGINARY'),
    ('nonassoc','TWO_POST_EX_CAST'),
    ('left','POST_INCR','POST_DECR'),
)

def p_ex_integer(p):
    '''primary_expression : DEC
                          | HEX
                          | BIN
    '''
    p[0] = ('int',p[1])

def p_ex_float(p):
    '''primary_expression : FLOAT
    '''
    p[0] = ('float',p[1])

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = ('identifier',p[1])

def p_ex_identifier(p):
    '''primary_expression : identifier'''
    p[0] = p[1]

def p_ex_factor(p):
    '''primary_expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_upcasting(p):
    '''expression : assign_expression %prec EX_CAST
       assign_expression : binop_expression %prec ASS_EX_CAST
       binop_expression : unary_expression %prec BIN_EX_CAST
       unary_expression : two_unary_expression %prec UN_EX_CAST
       two_unary_expression : postfix_expression %prec TWO_UN_EX_CAST
       postfix_expression : two_postfix_expression %prec TWO_POST_EX_CAST
       two_postfix_expression : primary_expression %prec POST_EX_CAST
    '''
    p[0] = p[1]

def p_ex_assign(p):
    '''assign_expression : identifier ASSIGN expression
    '''
    p[0] = ('assign',p[2],p[1],p[3])

def p_ex_binop(p):
    '''binop_expression : binop_expression PLUS binop_expression
                  | binop_expression MINUS binop_expression
                  | binop_expression TIMES binop_expression
                  | binop_expression CEIL_DIVIDE binop_expression
                  | binop_expression FLOOR_DIVIDE binop_expression
                  | binop_expression DIVIDE binop_expression
                  | binop_expression GREATER_THAN binop_expression
                  | binop_expression LESS_THAN binop_expression
                  | binop_expression GREATER_EQUAL binop_expression
                  | binop_expression LESS_EQUAL binop_expression
                  | binop_expression EQUAL binop_expression
                  | binop_expression NOT_EQUAL binop_expression
                  | binop_expression AND binop_expression
                  | binop_expression OR binop_expression
                  | binop_expression XOR binop_expression
                  | binop_expression MODULO binop_expression
    '''
    p[0] = ('binop',p[2],p[1],p[3])

def p_ex_binop_twochar(p):
    '''binop_expression : binop_expression TIMES TIMES binop_expression %prec POWER
    '''
    p[0] = ('binop_two',p[2]+p[3],p[1],p[4])

def p_ex_post_unop(p):
    '''postfix_expression : postfix_expression IMAGINARY
    '''
    p[0] = ('post_unop',p[2],p[1])

def p_ex_post_unop_twochar(p):
    '''two_postfix_expression : two_postfix_expression PLUS PLUS %prec POST_INCR
                              | two_postfix_expression MINUS MINUS %prec POST_DECR
    '''
    p[0] = ('post_unop_two',p[2]+p[3],p[1])

def p_ex_pre_unop(p):
    '''unary_expression : NOT unary_expression
                        | PLUS unary_expression %prec PRE_PLUS
                        | MINUS unary_expression %prec PRE_MINUS
    '''
    p[0] = ('pre_unop',p[1],p[2])

#def p_ex_pre_unop_twochar(p):
#    '''two_unary_expression : PLUS PLUS two_unary_expression %prec PRE_INCR
#                            | MINUS MINUS two_unary_expression %prec PRE_DECR
#    '''
#    p[0] = ('pre_unop',p[1]+p[2],p[3])

def p_error(p):
    print("Syntax error in input!")

parser = yacc()




   
