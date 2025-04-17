from ply.lex import lex

reserved = {
'and' : 'AND',
'or'  : 'OR',
'not' : 'NOT',
'xor' : 'XOR',
'nand': 'NAND',
'nor' : 'NOR',
'mod' : 'MODULO',
}

tokens = ['IDENTIFIER','DECIMAL','HEX','BINARY','FLOAT','EXPONENT_FLOAT'
         ,'IMAGINARY','PLUS','MINUS','TIMES'
         ,'CEIL_DIVIDE','FLOOR_DIVIDE','DIVIDE'
         ,'LPAREN','RPAREN','PREFIX_MINUS'
         ,'ABSOLUTE','POWER','POST_DEC','POST_INC'
         ,'GREATER_THEN','LESS_THEN','LESS_EQUAL','GREATER_EQUAL'
         ,'EQUAL','NOT_EQUAL','ASSIGN','COMMENT'] + list(reserved.values())


##### Basics #####
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

def t_COMMENT(t):
    r'\#[^#]*\#'
    pass

def t_FLOAT(t):
    r'\d+\.\d+'
    return t

t_DECIMAL = r'0|[1-9][0-9]*'
t_HEX = r'0x0|0x[1-9A-F][0-9A-F]*'
t_BINARY = r'0b0|0b1[01]*'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'

t_CEIL_DIVIDE = r'\/'
t_FLOOR_DIVIDE = r'\\'
t_DIVIDE = r'\|'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PREFIX_MINUS = r'-'

t_GREATER_THEN = r'>'
t_LESS_THEN = r'<'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_EQUAL = r'='
t_NOT_EQUAL = r'!='
t_ASSIGN = r':='


##### SPECIALS #####
t_ABSOLUTE = r'\+'
t_POWER = r'\*\*'
t_IMAGINARY = r'imag'
t_EXPONENT_FLOAT = r'E\d+' #wie float?

def t_EXPONENT_FLOAT(t):
    r'\d+.\d+E\d+'
    return t

t_POST_DEC = r'--'
t_POST_INC = r'\+\+'

##### Organisation #####
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


##### Build Lexer #####
lexer = lex()

