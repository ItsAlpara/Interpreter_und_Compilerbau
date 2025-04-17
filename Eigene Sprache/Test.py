from Lexer import lexer

lexer.input('5+1+3 \n 6+2')

for token in lexer:
    print(token)

