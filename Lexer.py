from ply.lex import lex


reserved = {
'and' : 'AND',
'or'  : 'OR',
'not' : 'NOT',
'xor' : 'XOR',
'mod' : 'MODULO',
'imag': 'IMAGINARY',
'E'   : 'EXPONENTIAL',
'wenn': 'IF',
'gilt': 'THEN',
'sonst': 'ELSE',
'solange': 'WHILE',
'wiederhole' : 'WDH',
'fuer':'LOOP',
'in':'IN',
'lambda' : 'LAMBDA',
}


tokens = ['IDENTIFIER','FLOAT','BIN','HEX','DEC','PLUS','MINUS'
         ,'TIMES','CEIL_DIVIDE','FLOOR_DIVIDE','DIVIDE','LPAREN'
         ,'RPAREN','GREATER_THAN','LESS_THAN','LESS_EQUAL'
         ,'GREATER_EQUAL','EQUAL','NOT_EQUAL','ASSIGN'
         ,'PLUS_ASSIGN','MINUS_ASSIGN','TIMES_ASSIGN','CEIL_DIVIDE_ASSIGN'
         ,'FLOOR_DIVIDE_ASSIGN','DIVIDE_ASSIGN','MOD_ASSIGN','POWER_ASSIGN'
         ,'E_ASSIGN','ASSIGN_ASSIGN','GREATER_THAN_ASSIGN','LESS_THAN_ASSIGN'
         ,'LESS_EQUAL_ASSIGN','GREATER_EQUAL_ASSIGN','EQUAL_ASSIGN'
         ,'NOT_EQUAL_ASSIGN','OR_ASSIGN','XOR_ASSIGN','AND_ASSIGN'
         ,'LBRACE','RBRACE','SEMICOLON','POINT','COMMA','LBRACKET','RBRACKET'
         ,'ARROW'] + list(reserved.values())


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

def t_MOD_ASSIGN(t):
    r'mod:='
    return t

def t_E_ASSIGN(t):
    r'E:='
    return t

def t_OR_ASSIGN(t):
    r'or:='
    return t

def t_XOR_ASSIGN(t):
    r'xor:='
    return t

def t_AND_ASSIGN(t):
    r'and:='
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

t_PLUS_ASSIGN = r'\+:='
t_MINUS_ASSIGN = r'-:='
t_TIMES_ASSIGN = r'\*:='
t_CEIL_DIVIDE_ASSIGN = r'\/:='
t_FLOOR_DIVIDE_ASSIGN = r'\\:='
t_DIVIDE_ASSIGN = r'\|:='
t_POWER_ASSIGN = r'\*\*:='

t_ASSIGN_ASSIGN = r':=:='

t_GREATER_THAN_ASSIGN = r'>:='
t_LESS_THAN_ASSIGN = r'<:='
t_LESS_EQUAL_ASSIGN = r'<=:='
t_GREATER_EQUAL_ASSIGN = r'>=:='
t_EQUAL_ASSIGN = r'=:='
t_NOT_EQUAL_ASSIGN = r'!=:='

t_POINT = r'\.'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'


######### SEQUENCE ##############
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'

######### LAMBDA ################
t_ARROW = r'->'

##### Organisation #####

#t_ignoreCMT = r'\#[^#]*\#'
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

##### Build Lexer #####
lexer = lex()
