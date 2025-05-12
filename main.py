###Datum: 07.05.2025
###Autor: Alpara
###Version: 5.0f


from Lexer import lexer
from Parser import parser
from Interpreter import evalu

state = {"x": 0,"y":0,"z":0}

def outPrint(zahl):
    match(zahl):

        ### Test Lexer ###
        case(1):
            while True:
                s = input('input > ')
                lexer.input(s)
                if (s == 'exit'):
                    break
                for tok in lexer:
                    if not tok:
                        break
                    print(tok)


        ### Test Parser ###
        case(2):
            while True:
                try:
                    s = input('input > ')
                    if(s == 'exit'):
                        break
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
                    if(s == 'exit'):
                        break
                    if(s == 'dict'):
                        print(state)
                        break
                except EOFError:
                    break
                if not s: continue

                result = evalu(parser.parse(s), state)
                print(result)

while True:
    try:
        z = int(input("Gib eine Zahl ein: "))
        outPrint(z)
    except ValueError:
        print("Bitte eine gültige ganze Zahl eingeben!")

