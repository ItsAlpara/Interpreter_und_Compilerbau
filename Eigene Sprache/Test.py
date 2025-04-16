from Lexer import lexer

lexer.input(r'5+6i')

for token in lexer:
    print(token)

