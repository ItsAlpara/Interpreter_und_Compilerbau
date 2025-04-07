from lex_test import lexer

lexer.input("5")

for token in lexer:
    print(token)