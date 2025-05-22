from Lexer import tokens
from ply.yacc import yacc

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('nonassoc','COMP_EXPR'),
    ('left', 'EQUAL', 'NOT_EQUAL', 'GREATER_THAN', 'LESS_THAN', 'GREATER_EQUAL', 'LESS_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'CEIL_DIVIDE', 'FLOOR_DIVIDE', 'MODULO'),
    ('left', 'POWER','EXPONENTIAL'),
    ('left', 'IMAGINARY'),
    ('right', 'NOT', 'UPLUS', 'UMINUS'),
    ('nonassoc', 'IDENT_EXPR')
)


def p_ex_integer(p):
    '''expression : DEC
                  | HEX
                  | BIN '''
    p[0] = ('int', p[1])


def p_ex_float(p):
    '''expression : FLOAT
    '''
    p[0] = ('float', p[1])


def p_identifier(p):
    '''identifier : IDENTIFIER
    '''
    p[0] = ('identifier', p[1])


def p_ex_identifier(p):
    '''expression : identifier %prec IDENT_EXPR'''
    p[0] = p[1]


def p_ex_factor(p):
    '''expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_ex_assign(p):
    '''expression : identifier ASSIGN expression
                  | identifier PLUS_ASSIGN expression %prec ASSIGN
                  | identifier MINUS_ASSIGN expression %prec ASSIGN
                  | identifier TIMES_ASSIGN expression %prec ASSIGN
                  | identifier CEIL_DIVIDE_ASSIGN expression %prec ASSIGN
                  | identifier FLOOR_DIVIDE_ASSIGN expression %prec ASSIGN
                  | identifier DIVIDE_ASSIGN expression %prec ASSIGN
                  | identifier MOD_ASSIGN expression %prec ASSIGN
                  | identifier POWER_ASSIGN expression %prec ASSIGN
                  | identifier E_ASSIGN expression %prec ASSIGN
                  | identifier ASSIGN_ASSIGN expression %prec ASSIGN
                  | identifier GREATER_THAN_ASSIGN expression %prec ASSIGN
                  | identifier LESS_THAN_ASSIGN expression %prec ASSIGN
                  | identifier LESS_EQUAL_ASSIGN expression %prec ASSIGN
                  | identifier GREATER_EQUAL_ASSIGN expression %prec ASSIGN
                  | identifier EQUAL_ASSIGN expression %prec ASSIGN
                  | identifier NOT_EQUAL_ASSIGN expression %prec ASSIGN
                  | identifier OR_ASSIGN expression %prec ASSIGN
                  | identifier XOR_ASSIGN expression %prec ASSIGN
                  | identifier AND_ASSIGN expression %prec ASSIGN
    '''
    p[0] = ('assign',p[2],p[1],p[3])


def p_ex_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression CEIL_DIVIDE expression
                  | expression FLOOR_DIVIDE expression
                  | expression DIVIDE expression
                  | expression AND expression
                  | expression OR expression
                  | expression XOR expression
                  | expression MODULO expression
                  | expression EXPONENTIAL expression
    '''
    p[0] = ('binop', p[2], p[1], p[3])


def p_ex_binop_twochar(p):
    '''expression : expression TIMES TIMES expression %prec POWER
    '''
    p[0] = ('binop_two', p[2] + p[3], p[1], p[4])


def p_ex_post_unop(p):
    '''expression : expression IMAGINARY
    '''
    p[0] = ('post_unop', p[2], p[1])


def p_ex_pre_unop(p):
    '''expression : NOT expression
                  | PLUS expression %prec UPLUS
                  | MINUS expression %prec UMINUS
    '''
    p[0] = ('pre_unop', p[1], p[2])

def p_ex_compartor_seq(p):
    '''expression : ex_comp %prec COMP_EXPR
    '''
    p[0]=('comp_seq',p[1])

def p_ex_comp(p):
    '''ex_comp : expression GREATER_THAN expression
               | expression LESS_THAN expression
               | expression GREATER_EQUAL expression
               | expression LESS_EQUAL expression
               | expression EQUAL expression
               | expression NOT_EQUAL expression
    '''
    p[0]=(p[1],p[2],p[3])

def p_ex_comp_seq(p):
    '''ex_comp : ex_comp GREATER_THAN expression
               | ex_comp LESS_THAN expression
               | ex_comp GREATER_EQUAL expression
               | ex_comp LESS_EQUAL expression
               | ex_comp EQUAL expression
               | ex_comp NOT_EQUAL expression
    '''
    p[0]=p[1]+(p[2],p[3])

################################ SEQUENCES ####################################
def p_sequence_body(p):
    '''expression : LBRACE sequence RBRACE'''
    p[0] = ('sequence_body', p[2])

def p_sequence_exp_sem_cast(p):
    '''sequence : expression
                | expression SEMICOLON
    '''
    p[0] = ('ex_sem',p[1])


def p_sequence_ex_sem_seq(p):
    '''sequence : expression SEMICOLON sequence'''
    p[0] = ('ex_sem_seq',p[1],p[3])

############################### CONTROL STRUCTURES #############################
def p_ex_if(p):
    '''expression : IF expression THEN COMMA expression POINT
    '''
    p[0] = ('if',p[2],p[5])

def p_ex_if_else(p):
    '''expression : IF expression THEN COMMA expression COMMA ELSE expression POINT
    '''
    p[0] = ('if_else',p[2],p[5],p[8])

def p_ex_while(p):
    '''expression : WHILE expression THEN COMMA expression POINT
    '''
    p[0] = ('while',p[2],p[5])

def p_brackets(p):
    '''brack : LBRACKET
             | RBRACKET
    '''
    p[0] = ('brack',p[1])

def p_ex_loop(p):
    '''expression : LOOP identifier IN brack expression COMMA expression brack WDH expression POINT
    '''
    p[0]= ('loop',p[2],p[4],p[5],p[7],p[8],p[10])


################################################################################

#def p_def_lambda(p):
 #   '''expression : LAMBDA LPAREN 
  #  '''
    
############################### ERROR HANDELING ################################
    
def p_error(p):
   print("Syntax error in input!")

parser = yacc()


