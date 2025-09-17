import math

from sympy import evaluate

from Entry import *

def evalu(node, env):
    match node:

########################################################################################################################
################################### BASICS #############################################################################
########################################################################################################################

        case ['identifier',value]:      # Im identifier steht der Bezeichner der Variable und der Wert der Variable.
            return env[value].value     # Diese ist jedoch nur in der Umgebung sichtbar

        case ['int', value]:
            return int(value)           # Beim übergeben der Variable vom Paser geben wir den Wert als int cast zurück

        case ['float', value]:
            return float(value)         # Beim übergeben der Variable vom Paser geben wir den Wert als float cast zurück

        case ['assign', op, left, right]:       # Gimmicks, keine Erläuterung, da wie binop nur mit Zuweisung
            er = 0
            match op:
                case ':=':
                    er = evalu(right, env)
                case ':=:=':
                    er = evalu(right, env)
                case '+:=':
                    er = evalu(('binop','+',left,right), env)
                case '-:=':
                    er = evalu(('binop','-',left,right), env)
                case '*:=':
                    er = evalu(('binop','*',left,right), env)
                case '|:=':
                    er = evalu(('binop','|',left,right), env)
                case '/:=':
                    er = evalu(('binop','/',left,right), env)
                case '\\:=':
                    er = evalu(('binop','\\',left,right), env)
                case 'mod:=':
                    er = evalu(('binop','mod',left,right), env)
                case '**:=':
                    er = evalu(('binop_two','**',left,right), env)
                case 'E:=':
                    er = evalu(('binop','E',left,right), env)
                case '<:=':
                    er = evalu(('binop','<',left,right), env)
                case '>:=':
                    er = evalu(('binop','>',left,right), env)
                case '<=:=':
                    er = evalu(('binop','<=',left,right), env)
                case '>=:=':
                    er = evalu(('binop','>=',left,right), env)
                case '=:=':
                    er = evalu(('binop','=',left,right), env)
                case '!=:=':
                    er = evalu(('binop','!=',left,right), env)
                case 'or:=':
                    er = evalu(('binop','or',left,right), env)
                case 'xor:=':
                    er = evalu(('binop','xor',left,right), env)
                case 'and:=':
                    er = evalu(('binop','and',left,right), env)
            env[left[1]].value = er
            return er #             #

        case ['binop', op, left, right]:
            el = evalu(left, env)                       # Links komplett evaluieren vor Operation
            er = evalu(right, env)                      # Rechts komplett evaluieren vor Operation
            match op:
                case '+':
                    return el + er                      # Ergebnis der Addition von Links plus Rechts

                case '-':
                    return el - er                      # Ergebnis der Subtraktion von Links minus Rechts

                case '*':
                    return el * er                      # Ergebnis der Multiplikation von Links mal Rechts

                case '|':
                    return el / er                      # Ergebnis der Division Links durch Rechts

                case '/':
                    return math.ceil(el / er)           # Aufrundung des Ergebnisses der Division Links durch Rechts

                case '\\':
                    return math.floor(el / er)          # Abrundung des Ergebnisses der Division Links durch Rechts

                case '<=':
                    return int(el <= er)                # Links kleiner gleich rechts

                case '>=':
                    return int(el >= er)                # Links größer gleich rechts

                case '<':
                    return int(el < er)                 # Links echt kleiner rechts

                case '>':                               # Links echt größer rechts
                    return int(el > er)

                case '=':                               # Gleichheit von Links und rechts
                    return int(el == er)

                case '!=':                              # Ungleichheit von links und rechts
                    return int(el != er)

                case 'and':                             # nur 1, wenn beide True
                    if el == 0 or er == 0:
                        return 0
                    else:
                        return 1

                case 'or':
                    if el != 0 and er != 0:             # nur 1, wenn eins von beiden oder beide true
                        return 1
                    else:
                        return 0

                case 'xor':                             # nur eins, wenn beide unterschiedlich
                    if (el != 0 and er != 0) or (el == 0 and er == 0):
                        return 0
                    else:
                        return 1

                case 'mod':
                    return el % er                      # links mod rechts

                case 'E':
                    return el * (10**er)                # Angepasst E als OP

        case ['binop_two', op, left, right]:            # POWER !!!!
            el = evalu(left, env)                       # Zuerst links
            er = evalu(right, env)                      # und rechts komplett evaluieren
            match(op):
                case('**'):
                    return el ** er                     #dann POWER!!

        case ['post_unop', 'imag', operand]:
            return complex(0,operand[1])

        case ['pre_unop', op, operand]:                 # Vorzeichenregeln
            match op:
                case '+':                               # Plus nimmt den Absolutwert
                    return abs(evalu(operand, env))
                case '-':                               # Minus dreht jedes mal das Vorzeichen
                    return -evalu(operand, env)
                case 'not':                             # not gibt einen 0 wenn es alles außer 0 ist, sonst 1.
                    return 0 if evalu(operand, env) != 0 else 1

########################################################################################################################
################################### SEQUENCE ###########################################################################
########################################################################################################################

        case ['seq',body]:
            for expr in body[:-1]:              # Wir gehen jede Expression, bis auf die letzte durch und werten diese
                evalu(expr, env)                # dann aus.
            return evalu(body[-1], env)         # Hier wird explizit nur noch die letzte ausgewählt und zurückgegeben

########################################################################################################################
################################### CONTROL STRUCTURES #################################################################
########################################################################################################################
        case ['if', cond, expr]:                # Wenn cond wahr: return ergebnis, sonst passiert nichts
            return evalu(expr,env) if evalu( cond, env) == True else None #Prompt: {x:=3;wenn x = 3 gilt, y:=2 .}

        case ['if_else', cond, expr, expr2]:     # Wenn cond wahr: return ergebnis, sonst return zweites ergebnis
            return evalu(expr,env) if evalu(cond, env) == True else evalu( expr2, env)

        case ['while', cond, expr]:             # Wenn cond wahr iteriere, solange die cond wahr ist und evaluiere die
            result = None                       # expr so lange und gib sie am Ende aus
            while(cond == True):
                result = evalu( expr, env)
            return result

        case ['loop',init,end,do]:             # Führe loop so lange bis zum Endwert aus
            i = int(evalu(init, env))          # Angeben des Initialwertes
            e = int(evalu(end,env))            # Berechnen des Endergebnisses
            result = None                      # Anlegen des Rückgabewertes

            if i == None: return result                     # Wenn kein Initialwert da ist, geben wir None zurück

            for _ in range(e):
                result = evalu(do,env)
            return result

        case ['pointloop',init,von,bis,do]: # Prompt: {x:=0;fuer x in 2 .. 5 wiederhole x+:=1 .}
            i = int(evalu(init,env))
            v = int(evalu(von,env))
            b = int(evalu(bis,env))
            result = None

            if i == None: return result

            for _ in range(b-v):
                result = evalu(do, env)
            return result


########################################################################################################################
################################### LAMBDA #############################################################################
########################################################################################################################
        case ['lambda',variable,body]:
            return (env,variable,body)

########################################################################################################################
################################### CALL ###############################################################################
########################################################################################################################
        case ['call',function,parameter]:
            return None


    return None


