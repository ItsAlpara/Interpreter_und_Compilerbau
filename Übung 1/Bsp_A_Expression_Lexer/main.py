from a_expression_lexer import lexer

lexer.input("1+2-3+4321+1")

for token in lexer:
    print(token)

#lexer.input("3.14")

#for token in lexer:
#    print(token)
