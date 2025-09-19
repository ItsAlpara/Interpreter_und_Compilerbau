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
            return er

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
            for expr in body[:-1]:                 # Wir gehen jede Expression, bis auf die letzte durch und werten diese
                evalu(expr, env)                   # dann aus.
            return evalu(body[len(body)-1], env)   # Hier wird explizit nur noch die letzte ausgewählt und zurückgegeben

########################################################################################################################
################################### CONTROL STRUCTURES #################################################################
########################################################################################################################
    
        case ['if', cond, expr]:                # Wenn cond wahr: return ergebnis, sonst passiert nichts
            return evalu(expr,env) if evalu( cond, env) == 1 else None #Prompt: {x:=3;wenn x = 3 gilt, y:=2 .}

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
    
        case ['lambda',variable,body]:      # Hiermit können neue Funktionen erstellt werden. Hierbei speichert das  
            return (env,variable,body)      # aktuelle Environment die Symboltabelle. In Variablen stehen jene Variablen 
                                            # denen im Laufe des Programms Werte zugewiesen werden zu müssen, um die 
                                            # Funktion aufrufen zu können. Im Body steht das Programm welches 
                                            # auszuführen ist.

########################################################################################################################
################################### CALL ###############################################################################
########################################################################################################################
        case ['call',function,parameter]:

            (env_f, variable_f, body_f) = evalu(function, env)  # Wir suchen eine erzeugte Funktion in unserer
                                                                # aktuellen Symboltabelle und speichern die Symboltabelle,
                                                                # die Variablen und den body in dem Triple.

            # Wir erzeugen uns ein neues Lambda und weisen diesem die notendigen Informationen zu

            variablelist = []                              # Leere Variablenliste
            oversupplyvar = None                           # Beim Oversupply alle Argumente in einer Variable speichern
            env_new = SymbolTable(parent=env_f)            # Neues Environment erzeugen mit aktuellem Env. als Parent
            rest_variables = ['paramlist']                  # Wichtig für Parser!

            # SETUP DER VARIABLEN

            for variable in variable_f[1]:                 # Für jede Variable (Identifier) in der oberen Variablenliste
                variablelist.append(variable[1])           # Wir nehmen uns aus diesen Tupeln die Bezeichner und
                                                           # speichern diese in der Variablenliste

            # OVERSUPPLY

            if variable_f[0] == 'paramlist_point':         # Falls Oversuplly geparsed wurde
                oversupplyvar = variable_f[2][1]           # Wir nehmen den Bezeichner der Oversupplyvariable
                env_new.put(oversupplyvar)                 # Wir fügen den Bezeichner in die Symboltabelle hinzu
                env_new[oversupplyvar].value = []          # Der Bezeichner kann nun eine Liste von Werten
                                                           # unter dem Bezeichner halten
                rest_variables = ['paramlist_point']        # Wichtig für Parser!


            # UNDERSUPPLY

            for variable in parameter:                      # Für jede Variable, die in Parameter übergeben wurden
                if variable[0] == 'callparam_assignment':   # Wenn wir dem Bezeichner einen Wert zuweisen wollen
                    if variable[1][1] in variablelist:      # Wenn der gefundene Bezeichner in der Parameterliste ist
                        val = evalu(variable[2], env)       # Wir evaluieren den übergebenen Parameter
                        env_new.put(variable[1][1])         # Wir fügen den Bezeichner aus dem Identifiertupel
                                                            # in unsere Symboltablle ein
                        env_new[variable[1][1]].value = val # Wir weisen dem Bezeichner in der Tabelle seinen
                                                            # evaluierten Wert zu
                        variablelist.remove(variable[1][1]) # Wir entfernen die Variable aus der noch übrigen
                                                            # Variablen aus der Variablenliste

            # OVERSUPPLY adding Variables (Zuweisung nach Reihenfolge der Variablenliste)

            for variable in parameter:                      # Für jede Variable, die in Parameter übergeben wurden
                if variable[0] == 'callparam_expr':         # Parser sagt uns es ist nur eine EXPR
                    val = evalu(variable[1], env)           # Wir evaluieren den Wert wer übergeben worden ist
                    try:
                        p = variablelist.pop(0)             # Wir nehmen des erste Element der Variablenliste heraus
                        env_new.put(p)                      # Stecken die Variable in unsere neue Symboltabelle
                        env_new[p].value = val              # und weisen ihm den evaluierten Wert zu
                    except IndexError:
                        if oversupplyvar is not None:       # Wenn Oversuppyvariable ist nicht None
                            env_new[oversupplyvar].value.append(val)        # Wir fügen der Symboltabelle unter dem
                                                                            # Bezeichner des Oversupply's eine Variable
                                                                            # zu im Fall, dass Variablenliste leer
                        else:
                            print('error: oversupply variable not found')   # Es wurde keine OversupplyVariable gefunden
                                                                            # wo der Wert hätte hinterlegt werden können

            # Zum Parsen, falls Undersupply vorliegt

            if variablelist:                                    # Wenn die Variablenliste nicht leer
                templist = []                                   # Temporäre Liste
                for variable in variablelist:                   # Für jede Variable in der Variablenliste
                    templist.append(('identifier', variable))   # Bringe die Bezeichner in ihr altes Format als Liste
                rest_variables.append(tuple(templist))          # Füge diese nun dem für den Parser benötigten Format an
                return (env_new, tuple(rest_variables), body_f) # Gib das neue environment
                                                                # mit den Restvariablen und dem body zurück
            return evalu(body_f, env_new)   #Versuchen mit dem neuen Environment und dem body zu evaluieren

########################################################################################################################
################################### LET ################################################################################
########################################################################################################################

        case['exp_let',letlist,body]:                           # Wir bekommen eine Liste von Parametern und einen Body
            identlist = [name[1] for name, _ in letlist]        # Wir erstellen eine List von allen Bezeichnern
            env_new = env.push(identlist)                       # Die Bezeichner werden in neue Symboltabelle angelegt
            for (name, expr) in letlist:                        # Für jedes Tupel Name und Expr in Letlist:
                value = evalu(expr, env_new)                    # Evaluieren wir den Wert im neuen Environment
                env_new[name[1]].value = value                  # und legen diesen unter dem Bezeichner in der Tabelle ab
            return evalu(body, env_new)                         # dann Evaluieren wir das Ergebnis mit dem neuen Env.


    return None


