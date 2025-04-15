from ply.lex import lex

tokens = ['NUMBER', 'PLUS', 'MINUS','FLOAT']

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_NUMBER    = r'\d+'


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_error(t):
    raise("unknown token")

lexer = lex()
