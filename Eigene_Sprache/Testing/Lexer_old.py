from ply.lex import lex

reserved = {
'and' : 'AND',
'or'  : 'OR',
'not' : 'NOT',
'xor' : 'XOR',
'nand': 'NAND',
'nor' : 'NOR',
'mod' : 'MODULO',
'imag': 'IMAGINARY',
}

tokens = ['IDENTIFIER','FLOAT','INTEGER'
         ,'PLUS','MINUS','TIMES','CEIL_DIVIDE','FLOOR_DIVIDE','DIVIDE'
         ,'LPAREN','RPAREN'
         ,'GREATER_THAN','LESS_THAN','LESS_EQUAL','GREATER_EQUAL'
         ,'EQUAL','NOT_EQUAL','ASSIGN','COMMENT'] + list(reserved.values())


##### Basics #####
def t_COMMENT(t):
    r'\#[^#]*\#'
    pass

def t_FLOAT(t):
    r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'(\d+)|(0x[0-9a-fA-F]+)|(0b[01]+)'
    t.value = int(t.value[2:],base=2) if t.value.startswith('0b') else (int(t.value[2:],base=16) if t.value.startswith('0x') else int(t.value))
    #t.value = eval(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
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

while True:
    s = input('input > ')
    lexer.input(s)
    for tok in lexer:
        if not tok:
            break
        print(tok)
