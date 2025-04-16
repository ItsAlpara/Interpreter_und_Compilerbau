from ply.lex import lex


tokens = ['DECIMAL','HEX','BINARY','FLOAT','E'
         ,'COMPLEX','PLUS','MINUS','TIMES'
         ,'CEIL_DIVIDE','FLOOR_DIVIDE','DIVIDE'
         ,'MODULO','LPAREN','RPAREN','PREFIX_MINUS'
         ,'ABSOLUTE','POWER','POST_DEC','POST_INC'
         ,'GREATER_THEN','LESS_THEN','LESS_EQUAL','GREATER_EQUAL'
         ,'EQUAL','NOT_EQUAL','ASSIGN','AND','OR','NOT','XOR','XAND',
          'FALSE','TRUE','COMMENT','COMMENT_MULTILINE',]

literals = [ '+','-','*','/' ]


t_DECIMAL = r'\d+'
t_HEX = r'0x'
t_BINARY = r'0b'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

t_COMPLEX = r'\d+i'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'

t_CEIL_DIVIDE = r'\/'
t_FLOOR_DIVIDE = r'\\'
t_DIVIDE = r'\|'

t_MODULO = r'mod'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PREFIX_MINUS = r'\-'
t_ABSOLUTE = r'\+'
t_POWER = r'\*\*'

t_POST_DEC = r'\-\-'
t_POST_INC = r'\+\+'

t_GREATER_THEN = r'>'
t_LESS_THEN = r'<'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_EQUAL = r'='
t_NOT_EQUAL = r'!='
t_ASSIGN = r'='

t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'
t_XOR = r'xor'
t_XAND = r'xand'

t_FALSE = r'0'
t_TRUE =  r'[a-zA-Z_][a-zA-Z0-9_]*]'

def t_COMMENT(t):
    r'\#.*'
    pass

def t_COMMENT_MULTILINE(t):
    r'\#.* \#.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex()

