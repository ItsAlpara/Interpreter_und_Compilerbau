from Lexer import lexer
from Parser import parser
from Interpreter import eval

while True:
    try:
        zahl = int(input("Gib eine Zahl ein: "))
        break
    except ValueError:
        print("Bitte eine gültige ganze Zahl eingeben!")

match(zahl):

### Test Lexer ###
    case(1):
        while True:
            s = input('input > ')
            lexer.input(s)
            for tok in lexer:
                if not tok:
                    break
                print(tok)


### Test Parser ###
    case(2):
        while True:
            try:
                s = input('input > ')
            except EOFError:
                break
            if not s: continue
            result = parser.parse(s)
            print(result)


### Test Interpreter ###
    case(3):
        while True:
            try:
                s = input('input > ')
            except EOFError:
                break
            if not s: continue

            result = eval(parser.parse(s))
            print(result)



