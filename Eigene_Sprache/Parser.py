from Lexer import tokens
from ply.yacc import yacc

precedence = (
    ('right','ASSIGN'),
    ('left','OR'),
    ('left','XOR'),
    ('left','AND'),
    ('left','EQUAL','NOT_EQUAL'),
    ('nonassoc','GREATER_THAN','LESS_THAN','GREATER_EQUAL','LESS_EQUAL'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','CEIL_DIVIDE','FLOOR_DIVIDE','MODULO'),
    ('left','POWER'),
    ('right','NOT','UPLUS','UMINUS'),
   # ('right','PRE_INCREMENT','PRE_DECREMENT'),
    ('left','IMAGINARY','POST_INCREMENT','POST_DECREMENT'),
    ('nonassoc','IDENT_EXPR')
)

def p_ex_integer(p):
    '''expression : DEC
                  | HEX
                  | BIN'''
    p[0] = ('int',p[1])

def p_ex_float(p):
    '''expression : FLOAT
    '''
    p[0] = ('float',p[1])

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = ('identifier',p[1])

def p_ex_identifier(p):
    '''expression : identifier %prec IDENT_EXPR'''
    p[0] = p[1]

def p_ex_factor(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_ex_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression CEIL_DIVIDE expression
                  | expression FLOOR_DIVIDE expression
                  | expression DIVIDE expression
                  | expression GREATER_THAN expression
                  | expression LESS_THAN expression
                  | expression GREATER_EQUAL expression
                  | expression LESS_EQUAL expression
                  | expression EQUAL expression
                  | expression NOT_EQUAL expression
                  | identifier ASSIGN expression
                  | expression AND expression
                  | expression OR expression
                  | expression XOR expression
                  | expression MODULO expression
    '''
    p[0] = ('binop',p[2],p[1],p[3])

def p_ex_binop_twochar(p):
    '''expression : expression TIMES TIMES expression %prec POWER
    '''
    p[0] = ('binop_two',p[2]+p[3],p[1],p[4])

def p_ex_post_unop(p):
    '''expression : expression IMAGINARY
    '''
    p[0] = ('post_unop',p[2],p[1])

def p_ex_post_unop_twochar(p):
    '''expression : expression PLUS PLUS %prec POST_INCREMENT
                  | expression MINUS MINUS %prec POST_DECREMENT
    '''
    p[0] = ('post_unop_two',p[2]+p[3],p[1])

def p_ex_pre_unop(p):
    '''expression : NOT expression
                  | PLUS expression %prec UPLUS
                  | MINUS expression %prec UMINUS
    '''
    p[0] = ('pre_unop',p[1],p[2])

#def p_ex_pre_unop_twochar(p):
    #'''expression : PLUS PLUS expression %prec PRE_INCREMENT
     #             | MINUS MINUS expression %prec PRE_DECREMENT
    #'''
   # p[0] = ('pre_unop',p[1]+p[2],p[3])

def p_error(p):
    print("Syntax error in input!")

parser = yacc()




   
