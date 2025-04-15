#  function fact(n)
#  return n > 0 and n * fact(n-1) or 1
#  end

from ply.lex import lex


tokens = ['NAME','FUNCTION','LPAREN','RPAREN','NUMBER','PLUS','MINUS','END','GREATER','TIMES','LESS','RETURN','OR','AND']


t_LPAREN        =  r'\('
t_RPAREN        =  r'\)'
t_PLUS          =  r'\+'
t_MINUS         =  r'-'
t_NUMBER        =  r'\d+'
t_GREATER       =  r'>'
t_TIMES         =  r'\*'
t_LESS          =  r'<'

def t_OR(t):
    r'or'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_AND(t):
    r'and'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_END(t):
    r'end'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

t_ignore        =  ' \t'

def t_error(t):
    raise("unknown token")


lexer = lex()




#reserved = {
#   'if' : 'IF',
#   'then' : 'THEN',
#   'else' : 'ELSE',
#   'while' : 'WHILE',
#}

#tokens = ['LPAREN','RPAREN',...,'ID'] + list(reserved.values())

#def t_ID(t):
#    r'[a-zA-Z_][a-zA-Z_0-9]*'
#    t.type = reserved.get(t.value,'ID')    # Check for reserved words
#    return t