import ply.yacc as yacc


import convertLangage
from Work import verifIfIsWord

reserved = {
    "FIND": "FIND",
    "WHERE": "WHERE",
    "LIMIT": "LIMIT",
    "CP": "CP",
    "TYPE": "TYPE",
    "AND": "AND",
    "SELECT": "SELECT",
    "FROM": "FROM"
}

# Tokens


t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_EQUAL = r'='
t_NUMBER = r'\d'



tokens = [
             'NUMBER',  'NAME', 'COMMA', "ENTITY" , "POSTAL", "SEMICOLON", "EQUAL",  "INFO"
         ] + list(reserved.values())




# Ignored characters
t_ignore = " \t"


def t_ENTITY(t):
    r"""DESC|URL_INFO|ID|PLACE|TITLE|\*"""
    return t

def t_POSTAL(t):
    r'''\d{2}[ ]?\d{3}'''
    return t

def t_INFO(t):
    r'''([A-Za-z-_0-9])*\/([A-Za-z-_0-9])*\/([A-Za-z-_0-9])*'''
    return t


def t_NAME(t):
    r'[\/a-zA-Z_][\/a-zA-Z_0-9-]*'
    t.type = reserved.get(t.value, 'NAME')  # Check for reserved words
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer

import ply.lex as lex
# lexer = lex.lex(debug=1) #add
lex.lex()


def p_start(p):
    """start : statement """
    p[0] = ('START', p[1])
    convertLangage.convertLanguage(p[1])


def p_satement_expr(p):
    """statement :  FIND  ENTITIES WHERE CONDITION SEMICOLON
    | FIND  ENTITIES WHERE CONDITION  LIMIT NUMBER SEMICOLON
    | SELECT ENTITIES FROM ENTITY EQUAL INFO """
    if len(p) == 6 and p[1] == "FIND":
        p[0] = ('FIND', p[2], p[4])
    elif len(p) == 8 and p[1] == "FIND":
        p[0] = ('FIND', p[2], p[4], int(p[6]))
    elif p[1] == "SELECT":
        p[0] = ('SELECT', p[2], p[6])


def p_expression_condition(p):
    '''CONDITION  : CP EQUAL POSTAL AND  WORK '''
    p[0] = ("CONDITION", p[3], p[5])

def p_error(p):
    print("error" +  str(p))


def p_expression_work(p):
    '''WORK :  TYPE EQUAL NAME '''
    if verifIfIsWord(p[3]) == -1:
        p.lexer.skip(1)
    else:
        p[0] = p[3]

def p_expression_expr(p):
    '''ENTITIES : ENTITY
    | ENTITIES COMMA ENTITY '''
    if len(p) == 2:
        p[0] = ("ENTITY", p[1], "EMPTY")
    else:
        p[0] = ("ENTITY", p[1], p[3])


yacc.yacc()
#yacc.yacc(tabmodule="foo")  # after
s5: str = " FIND * WHERE  CP = 78300 AND TYPE = nothing LIMIT 0 ;" # error
s6: str = " FIND * WHERE  CP = 78300 AND TYPE = aide-personnes-handicapees LIMIT 1 ;" # work
s7: str = " FIND * WHERE  CP = 78300 AND TYPE = aide-personnes-handicapees LIMIT 0 ;" # create empty xml  ;) I choice the solution
s8: str = " FIND * WHERE  CP = 78300 AND TYPE = cours-tango LIMIT 1 ;"
s9: str = "SELECT * FROM TITLE = cours-tango/saint-germain-en-laye-78/couple-de-danseurs-de-tango-argentin-donne-cours-en-region-ouest-parisienne-2nq9"
#s = input('> ')
yacc.parse(s9)