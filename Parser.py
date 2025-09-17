from Lexer import tokens
from ply.yacc import yacc


#Precedence Tabelle zur Festlegung welche der Regeln höherwertiger sind in der Auswertung als eine Andere
#Je weiter unten, desto höherwertiger
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
#    ('left', 'AMPERSAND'),
    ('right', 'NOT', 'UPLUS', 'UMINUS'), #'LENGTH','ECHO','LIST'
    ('left', 'IMAGINARY'), #,'LIST_GET'
    ('right','LPAREN','RPAREN'),
    ('nonassoc', 'IDENT_EXPR'),
)
########################################################################################################################
################################### BASICS #############################################################################
########################################################################################################################

def p_ex_integer(p):                                  #Regel für die Erstellung der Zahlen
    '''expression : DEC
                  | HEX
                  | BIN '''
    p[0] = ('int', p[1])

def p_ex_float(p):                                    #Regel für die Erstellung von Floats
    '''expression : FLOAT
    '''
    p[0] = ('float', p[1])

#def p_ex_string(p):                                   #Regel für die Erstellung von Strings
#    '''expression : STRING
#   '''
#    p[0] = ('string',p[1])

def p_identifier(p):                                  #Regel für die Erstellung eines Identifiers
    '''identifier : IDENTIFIER
    '''
    p[0] = ('identifier', p[1])

def p_ex_identifier(p):                               #Caste einen identifier zur Expression
    '''expression : identifier %prec IDENT_EXPR'''
    p[0] = p[1]

def p_ex_factor(p):                                   #Regeln für Klammerungen
    '''expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

########################################################################################################################
################################### OPERATIONS #########################################################################
########################################################################################################################


def p_ex_assign(p):                                   #Gimmick implementationen
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

def p_ex_binop(p):                                  #Einfache Implementation der Regeln für binäre Operatoren
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

def p_ex_binop_twochar(p):                              #POWER!!!
    '''expression : expression TIMES TIMES expression %prec POWER
    '''
    p[0] = ('binop_two', p[2] + p[3], p[1], p[4])

def p_ex_post_unop(p):                                  # Aufbau der Imaginären Zahlen
    '''expression : expression IMAGINARY
    '''
    p[0] = ('post_unop', p[2], p[1])

def p_ex_pre_unop(p):                                   # Vorzeichen Regeln
    '''expression : NOT expression
                  | PLUS expression %prec UPLUS
                  | MINUS expression %prec UMINUS
    '''
    p[0] = ('pre_unop', p[1], p[2])

def p_ex_compartor_seq(p):                              # Um mehrere Comparatoren hinteinander auswerten zu können
    '''expression : ex_comp %prec COMP_EXPR
    '''
    p[0]=('comp_seq',p[1])

def p_ex_comp(p):                                       #Comparator
    '''ex_comp : expression GREATER_THAN expression
               | expression LESS_THAN expression
               | expression GREATER_EQUAL expression
               | expression LESS_EQUAL expression
               | expression EQUAL expression
               | expression NOT_EQUAL expression
    '''
    p[0]=(p[1],p[2],p[3])


########################################################################################################################
################################### SEQUENCE ###########################################################################
########################################################################################################################
def p_ex_seq(p):                                        # Aufbau der Sequence: {EXP}
    '''expression : LBRACE sequence RBRACE'''
    p[0]=('seq',p[2])

def p_ex_seq_body_1(p):                                 # Reduzierungen der Expression auf eine Sequence mit oder ohne Semikolon
    '''sequence : expression
                | expression SEMICOLON
    '''
    p[0]= (p[1])

def p_ex_seq_body_2(p):                                 # Mehrere Expressions in der Sequenz: {EXP;EXP}
    '''sequence : expression SEMICOLON sequence
    '''
    p[0]= (p[1],p[3])


########################################################################################################################
################################### CONTROL STRUCTURES #################################################################
########################################################################################################################

def p_ex_if(p):                                         # Wenn EXP gilt, EXP .
    '''expression : IF expression THEN COMMA expression POINT
    '''
    p[0] = ('if',p[2],p[5])

def p_ex_if_else(p):                                    # WENN EXP gilt, EXP, sonst EXP .
    '''expression : IF expression THEN COMMA expression COMMA ELSE expression POINT
    '''
    p[0] = ('if_else',p[2],p[5],p[8])

def p_ex_while(p):                                      # solange exp gilt, exp .
    '''expression : WHILE expression THEN COMMA expression POINT
    '''
    p[0] = ('while',p[2],p[5])

def p_ex_loop(p):                                       #fuer IDENT in EXP wiederhole EXP .
    '''expression : LOOP identifier IN expression WDH expression POINT
    '''
    p[0]= ('loop',p[2],p[4],p[6])

def p_ex_loop_point(p):                                 #fuer IDENT in EXP .. EXP wiederhole EXP .
    '''expression : LOOP identifier IN expression POINT POINT expression WDH expression POINT
    '''
    p[0]=('pointloop',p[2],p[4],p[7],p[9])

########################################################################################################################
################################### LAMBDA #############################################################################
########################################################################################################################

def p_lambda(p):
    '''expression : LAMBDA LPAREN paramlist RPAREN ARROW expression %prec LAMBDAEXPR
    '''
    p[0] = ('lambda',p[3],p[6])

########################################################################
##### Wir wollen auch eine Liste von Parametern bei Lambda zulassen ####
######### Dafür sind die folgenden drei Methoden zuständig #############
########################################################################

def p_lambda_param(p):              # Damit wir aus einem identifier einen Parameter machen können
    ''' params : identifier
    '''
    p[0] = (p[1],)

def p_lambda_paramlist(p):          # Grundstruktur um überhaupt mehrere Parameter angeben zu können
    ''' params : params COMMA identifier
    '''
    p[0] = p[1] + (p[3],)

def p_lambda_paramlist_fin1(p):     # Mache aus Paramtern eine Paramterliste, um diese verwenden zu können
    ''' paramlist : params
    '''
    p[0]=('paramlist',p[1])

#############################
#### Oversupplyhandeling ####
#############################

def p_lambda_paramlist_fin2(p):     # Spezialfall für mehrere Parameter hintereinander und ... für "Rest"
    ''' paramlist : params COMMA identifier POINT POINT POINT
    '''
    p[0]=('paramlist_point',p[1],p[3])

def p_lambda_paramlist_fin3(p):     # Spezialfall für einen Parameter hintereinander und ... für "Rest"
    ''' paramlist : identifier POINT POINT POINT
    '''
    p[0]=('paramlist_point',(),p[1])

########################################################################################################################
################################### CALL ###############################################################################
########################################################################################################################

def p_ex_call(p):               # Aufbau zum Aufruf eines Calls
    ''' expression : expression LPAREN callparamlist RPAREN
    '''
    p[0] = ('ex_call',p[1],p[3])

def p_call_param_assignment(p):  # Wir weisen beim Funktionsaufruf einer bestimmten Variable einen Wert zu
    ''' callparam : identifier COLON expression
    '''
    p[0] = ('callparam_assignment',p[1],p[3])

def p_call_param_expr(p):       # Reduce von expression auf parameter
    ''' callparam : expression'''
    p[0] = ('callparam_expr',p[1])

def p_call_param_list_1(p):     # Reduce von parameter zu einer paramterliste
    ''' callparamlist :  callparam
    '''
    p[0]=(p[1],)

def p_call_param_list_2(p):     # mehrere Paramter hintereinander möglich machen
    ''' callparamlist :  callparamlist COMMA callparam
    '''
    p[0]= p[1] + (p[3],)

########################################################################################################################
################################### ERROR HANDELING ####################################################################
########################################################################################################################
    
def p_error(p):
   print("Syntax error in input!")

parser = yacc()


