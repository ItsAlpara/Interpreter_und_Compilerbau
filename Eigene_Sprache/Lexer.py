from ply.lex import lex

reserved = {
'and' : 'AND',
'or'  : 'OR',
'not' : 'NOT',
'xor' : 'XOR',
'mod' : 'MODULO',
'imag': 'IMAGINARY',
'E'   : 'EXPONENTIAL'
}

tokens = ['IDENTIFIER','FLOAT','BIN','HEX','DEC','PLUS','MINUS'
         ,'TIMES','CEIL_DIVIDE','FLOOR_DIVIDE','DIVIDE','LPAREN'
         ,'RPAREN','GREATER_THAN','LESS_THAN','LESS_EQUAL'
         ,'GREATER_EQUAL','EQUAL','NOT_EQUAL','ASSIGN'
         ,'LBRACE','RBRACE','SEMICOLON'] + list(reserved.values())


##### Basics #####

def t_BIN(t):
    r'0b[01]+'
    t.value = int(t.value, 2)
    return t
    
def t_HEX(t):
    r'0x([a-fA-F]|\d)+'
    t.value = int(t.value,16)
    return t

def t_FLOAT(t):
    #r'[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_DEC(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_\u007F-\uFFFF][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_CEIL_DIVIDE = r'\/'
t_FLOOR_DIVIDE = r'\\'
t_DIVIDE = r'\|'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_GREATER_THAN = r'>'
t_LESS_THAN = r'<'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_EQUAL = r'='
t_NOT_EQUAL = r'!='


t_ASSIGN = r':='

######SEQUENCE #######
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'



##### Organisation #####

def t_COMMENT(t):
   r'\#.*?\#'
   pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

##### Build Lexer #####
lexer = lex()