from Lexer import tokens
from ply.yacc import yacc

precedence = (
    ('left', 'LAMBDAEXPR'),
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('nonassoc','COMP_EXPR'),
    ('left', 'EQUAL', 'NOT_EQUAL', 'GREATER_THAN', 'LESS_THAN', 'GREATER_EQUAL', 'LESS_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'CEIL_DIVIDE', 'FLOOR_DIVIDE', 'MODULO'),
    ('left', 'POWER','EXPONENTIAL'),
    ('left', 'AMPERSAND'),
    ('right', 'NOT', 'UPLUS', 'UMINUS','LENGTH','ECHO','LIST'),
    ('left', 'IMAGINARY','LIST_GET'),
    ('right','LPAREN','RPAREN'),
    ('nonassoc', 'IDENT_EXPR'),
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

def p_ex_string(p):
    '''expression : STRING
    '''
    p[0] = ('string',p[1])


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
    '''expression : identifier ASSIGN expression %prec ASSIGN
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

############################### LAMBDA #########################################

def p_lambda_ex(p):
    ''' expression : LAMBDA LPAREN paramlist RPAREN ARROW expression %prec LAMBDAEXPR
    '''
    p[0] = ('ex_lambda',p[3],p[6])

def p_lambda_param(p):
    ''' params : identifier
    '''
    p[0] = (p[1],)

def p_lambda_paramlist(p):
    ''' params : params COMMA identifier
    '''
    p[0] = p[1] + (p[3],)

def p_lambda_paramlist_fin1(p):
    ''' paramlist : params
    '''
    p[0]=('paramlist',p[1])

def p_lambda_paramlist_fin2(p):
    ''' paramlist : params COMMA identifier POINT POINT POINT
    '''
    p[0]=('paramlist_point',p[1],p[3])

def p_lambda_paramlist_fin3(p):
    ''' paramlist : identifier POINT POINT POINT
    '''
    p[0]=('paramlist_point',(),p[1])

#################################  CALL ####################################################
def p_ex_call(p):
    ''' expression : expression LPAREN callparamlist RPAREN
    '''
    p[0] = ('ex_call',p[1],p[3])

def p_call_param_assignment(p):
    ''' callparam : identifier COLON expression
    '''
    p[0] = ('callparam_assignment',p[1],p[3])

def p_call_param_expr(p):
    ''' callparam : expression'''
    p[0] = ('callparam_expr',p[1])

def p_call_param_list_1(p):
    ''' callparamlist :  callparam
    '''
    p[0]=(p[1],)

def p_call_param_list_2(p):
    ''' callparamlist :  callparamlist COMMA callparam
    '''
    p[0]= p[1] + (p[3],)

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

def p_ex_loop(p):
    '''expression : LOOP identifier IN expression WDH expression POINT
    '''
    p[0]= ('loop',p[2],p[4],p[6])

def p_ex_loop_point(p):
    '''expression : LOOP identifier IN expression POINT POINT expression WDH expression POINT
    '''
    p[0]=('pointloop',p[2],p[4],p[7],p[9])

############################### ARRAY ##########################################

def p_ex_arr_def(p):
    '''expression : LBRACKET expr_arr RBRACKET
    '''
    p[0] = ('arr',p[2])

def p_ex_empty_arr_def(p):
    '''expression : LBRACKET RBRACKET
    '''
    p[0] = ('arr',())

def p_arr_expr_arr1(p):
    '''expr_arr : expr_arr COMMA expression
    '''
    p[0] = p[1] + (p[3],)

def p_arr_expr_arr2(p):
    '''expr_arr : expression
    '''
    p[0] = (p[1],)

def p_ex_list_get(p):
    '''expression : expression LBRACKET expression RBRACKET %prec LIST_GET
    '''
    p[0] = ('list_get',p[1],p[3])

def p_ex_list_get_plus(p):
    '''expression : expression LBRACKET PLUS RBRACKET %prec LIST_GET
    '''
    p[0] = ('rest_list_get',p[1])

def p_ex_list_len(p):
    '''expression : LENGTH expression'''
    p[0] = ('list_len',p[2])

############################### LISTS ##########################################

def p_ex_list(p):
    '''expression : LPAREN expr_list RPAREN
    '''
    p[0] = ('list',p[2])

def p_ex_empty_list(p):
    '''expression : NIL
    '''
    p[0] = None

def p_ex_list_def1(p):
    '''expr_list : expression COMMA expr_list
    '''
    p[0] = (p[1],p[3])

def p_ex_list_def2(p):
    '''expr_list : expression
    '''
    p[0] = (p[1],None)

def p_ex_cons(p):
    '''expression : expression AMPERSAND expression 
    '''
    p[0]=('cons',p[1],p[3])

def p_ex_list_op(p):
    '''expression : LIST expression
    '''
    p[0] = ('list',(p[2],None))

############################### MISC ###########################################

def p_ex_echo(p):
    '''expression : ECHO expression
    '''
    p[0]= ('echo',p[2])


############################ LET ##############################################
def p_exp_let(p):
    '''expression : LET letlist IN expression POINT
    '''
    p[0] = ('exp_let',p[2],p[4])

def p_letlist(p):
    '''letlist : identifier EQUAL expression
    '''
    p[0] = ((p[1],p[3]),)
    
def p_letlist2(p):
    '''letlist : letlist COMMA identifier EQUAL expression
    '''
    p[0] = p[1] + ((p[3],p[5]),)

############################### STRUCTS ########################################
def p_exp_struct(p):
    '''expression : STRUCT LBRACE idenlist RBRACE
    '''
    p[0] = ('struct',p[3])

def p_idenlist1(p):
    '''idenlist : identifier COLON expression
    '''
    p[0] = ((p[1],p[3]),)

def p_idenlist2(p):
    '''idenlist : idenlist COMMA identifier COLON expression
    '''
    p[0] = p[1] + ((p[3],p[5]),)

def p_exp_struct_access(p):
    '''expression : expression POINT identifier
    '''
    p[0] = ('structaccess',p[1],p[3])
    
############################### ERROR HANDELING ################################
    
def p_error(p):
   print("Syntax error in input!")

parser = yacc()


