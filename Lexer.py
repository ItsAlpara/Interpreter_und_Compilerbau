from ply.lex import lex


reserved = {                        #Reserved Tokens sind Bezeichnungen, welche nicht mehr für Variablenbezeichnungen
'and' : 'AND',                      #verwendet werden können, da diese sonst bei einer Doppelbelegung nicht
'or'  : 'OR',                       #unterschieden werden kann um was es sich letzten endes handelt.
'not' : 'NOT',
'xor' : 'XOR',
'mod' : 'MODULO',
'imag': 'IMAGINARY',
'E'   : 'EXPONENTIAL',
'wenn': 'IF',
'gilt': 'THEN',
'sonst': 'ELSE',
'solange': 'WHILE',
'wiederhole' : 'WDH',
'fuer':'LOOP',
'in':'IN',
'lambda' : 'LAMBDA',
#'len':'LENGTH',
#'echo':'ECHO',
'sei' : 'LET',
#'leere' : 'NIL',
}


tokens = ['IDENTIFIER','FLOAT','BIN','HEX','DEC','PLUS','MINUS'                # Das ist unsere Liste von Tokens, welche
         ,'TIMES','CEIL_DIVIDE','FLOOR_DIVIDE','DIVIDE','LPAREN'               # beim Parsing für die für shift und
         ,'RPAREN','GREATER_THAN','LESS_THAN','LESS_EQUAL'                     # reduce notwendig sind. Mit ihnen bilden
         ,'GREATER_EQUAL','EQUAL','NOT_EQUAL','ASSIGN'                         # wir den genauen Aufbau der Sprache
         ,'PLUS_ASSIGN','MINUS_ASSIGN','TIMES_ASSIGN','CEIL_DIVIDE_ASSIGN'
         ,'FLOOR_DIVIDE_ASSIGN','DIVIDE_ASSIGN','MOD_ASSIGN','POWER_ASSIGN'
         ,'E_ASSIGN','ASSIGN_ASSIGN','GREATER_THAN_ASSIGN','LESS_THAN_ASSIGN'
         ,'LESS_EQUAL_ASSIGN','GREATER_EQUAL_ASSIGN','EQUAL_ASSIGN'
         ,'NOT_EQUAL_ASSIGN','OR_ASSIGN','XOR_ASSIGN','AND_ASSIGN'
         ,'POINT','COMMA','LBRACE','RBRACE','SEMICOLON','COLON','ARROW'] + list(reserved.values())

# removed:  ,'LBRACKET','RBRACKET','STRING'

##### Basics #####

def t_BIN(t):                       # Implementation von Binären Zahlen von Python
    r'0b[01]+'
    t.value = int(t.value, 2)
    return t
    
def t_HEX(t):                       # Implementation von Hexadezimalzahlen Zahlen von Python
    r'0x([a-fA-F]|\d)+'
    t.value = int(t.value,16)
    return t

def t_FLOAT(t):                     # Implementation von Float Zahlen von Python
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_IDENTIFIER(t):                # Implementation von Identifiers, also Variablennamen die vergeben werden können
    r'[a-zA-Z_\u007F-\uFFFF][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t


t_PLUS = r'\+'                      # Implementation des plus operators
t_MINUS = r'-'                      # Implementation des minus operators
t_TIMES = r'\*'                     # Implementation des multiplikation operators
t_CEIL_DIVIDE = r'\/'               # Implementation des teilen aufrunden operators
t_FLOOR_DIVIDE = r'\\'              # Implementation des teilen abrunden operators
t_DIVIDE = r'\|'                    # Implementation des teilen operators

t_LPAREN = r'\('                    # Implementation der linken Klammer
t_RPAREN = r'\)'                    # Implementation der rechten Klammer

t_GREATER_THAN = r'>'               # Implementation von echt größer
t_LESS_THAN = r'<'                  # Implementation von echt kleiner
t_LESS_EQUAL = r'<='                # Implementation von größer gleich
t_GREATER_EQUAL = r'>='             # Implementation von kleiner gleich
t_EQUAL = r'='                      # Implementation von gleich
t_NOT_EQUAL = r'!='                 # Implementation von nicht gleich

t_ASSIGN = r':='                    #Implementation der Zuweisung

t_POINT = r'\.'                      # Implementation des Punkts
t_COMMA = r','                       # Implentation des Kommata
#t_LBRACKET = r'\['                  # Implementation der linken eckigen Klammer
#t_RBRACKET = r'\]'                  # Implementation der rechten eckigen Klammer

#t_STRING = r'("[^"]*")|' r"('[^']*')"   #Implementation von Strings



######### SEQUENCE ##############
t_SEMICOLON = r';'                  # Implementation des Semikolon für Sequenzen
t_LBRACE = r'{'                     # Implementation der linken geschweiften Klammer für Sequenzen
t_RBRACE = r'}'                     # Implementation der rechten geschweifen Klammer für Sequenzen

######### LAMBDA ################
t_ARROW = r'->'                    # Implementation eines Pfeils
t_COLON = r':'                     # Implementation des Doppelpunkts
##### Organisation #####

#t_ignoreCMT = r'\#[^#]*\#'
t_ignore = ' \t'                    # Implementation das escapes ignoriert werden

def t_newline(t):                   # Implementation das Zeilenumbrücke gestattet werden
    r'\n+'                          # und gibt an in welcher linie man sich befindet
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)




############# Gimmicks ##################################

def t_DEC(t):
    r'\d+'
    t.value = int(t.value)          #Implementation von Dezimalzahlen von Python
    return t

def t_MOD_ASSIGN(t):
    r'mod:='                        #Implementation von modulo assign
    return t

def t_E_ASSIGN(t):
    r'E:='                          #Implementation von E assign
    return t

def t_OR_ASSIGN(t):
    r'or:='                         #Implementation von OR assign
    return t

def t_XOR_ASSIGN(t):                #Implementation von XOR assign
    r'xor:='
    return t

def t_AND_ASSIGN(t):                #Implementation von AND assign
    r'and:='
    return t

t_PLUS_ASSIGN = r'\+:='             #Implementation von plus assign
t_MINUS_ASSIGN = r'-:='             #Implementation von minus assign
t_TIMES_ASSIGN = r'\*:='            #Implementation von times assign
t_CEIL_DIVIDE_ASSIGN = r'\/:='      #Implementation von ceil devide assign
t_FLOOR_DIVIDE_ASSIGN = r'\\:='     #Implementation von floor divide assign
t_DIVIDE_ASSIGN = r'\|:='           #Implementation von divide assign
t_POWER_ASSIGN = r'\*\*:='          #Implementation von power assign

t_ASSIGN_ASSIGN = r':=:='           #Implementation von assign assign

t_GREATER_THAN_ASSIGN = r'>:='      #Implementation von greater than assign
t_LESS_THAN_ASSIGN = r'<:='         #Implementation von less than assign
t_LESS_EQUAL_ASSIGN = r'<=:='       #Implementation von less equal assign
t_GREATER_EQUAL_ASSIGN = r'>=:='    #Implementation von greater equal assign
t_EQUAL_ASSIGN = r'=:='             #Implementation von equal assign
t_NOT_EQUAL_ASSIGN = r'!=:='        #Implementation von not equal assign




##### Build Lexer #####
lexer = lex()
