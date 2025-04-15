from lex_test import lexer

lexer.input("function fact(n) \n return n > 0 and n * fact(n-1) or 1 \n end")

for tokens in lexer:
    print(tokens)

