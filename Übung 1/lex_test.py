
#function fact(n)
#  return n > 0 and n * fact(n-1) or 1
#end

import ply.lex as lex

tokens = ['FUNCTION','WORD','PARAMETER','NUMBER','PLUS','MINUS','END']

t_FUNCTION      =  r'function'
t_PARAMETER     =  r'\([1-9][0-9]*\)'
t_WORD          =  r'[a-zA-Z_][a-zA-Z0-9_]*'
t_PLUS          =  r'\+'
t_MINUS         =  r'-'
t_NUMBER        =  r'\d+'
t_END           =  r'end'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_error(t):
    raise("unknown token")

lexer = lex()
