"""
bnf_declaration_specifier=""
bnf_declarator=""
bnf_declaration=""
bnf_compound_statement = ""



bnf_function_definition={"function-definition": ["{"+bnf_declaration_specifier["declaration-specifier"]+"}", bnf_declarator["declarator"], "{"+bnf_declaration["declaration"]+"}", bnf_compound_statement["compound-statement"]]}
bnf_external_declaration = {"external-declaration": [bnf_function_definition["function-definition"], bnf_declaration["declaration"]]}
bnf_translation_unit = {"translation-unit": ["{"+bnf_external_declaration["external-declaration"]+"}"]}
"""

import re
import collections

# p = re.compile('('+RE2+'|'+RE1+')');
# Token specification

# NUM = r'(?P<NUM>\d+)'
# PLUS = r'(?P<PLUS>\+)'
# MINUS = r'(?P<MINUS>-)'
# TIMES = r'(?P<TIMES>\*)'
# DIVIDE = r'(?P<DIVIDE>/)'
# LPAREN = r'(?P<LPAREN>\()'
# RPAREN = r'(?P<RPAREN>\))'
# WS = r'(?P<WS>\s+)'
# Token = collections.namedtuple('Token', ['type', 'value'])
#
# master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES,  DIVIDE, LPAREN, RPAREN, WS]))
# a = master_pat.scanner("2+1=3")
# for m in iter(a.match, None):
#     tok = Token(m.lastgroup, m.group())
#     print(tok)

# pattern = r"(<(\w*-*)*>)"
# master_pat = re.compile(pattern)

# element = text.split("::=")[1]
# temp_el = master_pat.findall(element)
#
# for te in temp_el:
#     # element = element.replace(te[0], "\"+\"r'\"+dict_bnf.get('"+te[0]+"', r'')+\"'\"+\"")
#     element = element.replace(te[0], "\"+dict_bnf.get(\"" + te[0] + "\", '')+\"")
#
# # dict_bnf[key] = element
# text = "dict_bnf['" + key +"'] = r\"(" + element +")\""

# from forest import NaryTree
#
# tree = NaryTree(key='1')
# branch1 = tree.add_child(key='1.1')
# branch2 = tree.add_child(key='1.2')
# branch11 = branch1.add_child(key='1.1.1')
#
# def do_something(node):
#     print(node)
#
# tree.traversal(visit=do_something)




storage_class_specifier = r'(auto|register|static|extern|typedef)'
PLUS = r'(\d+)'
sp = re.compile('(?P<sp>%s|%s)' % (PLUS, storage_class_specifier), re.I)

a = re.match(sp, "1AUTO123register")

print(a.group())


"""
bnf_dict[<translation-unit>] ::= "({%s})*" % bnf_dict.get("<external-declaration>", r"")

<external-declaration> ::= <function-definition> | <declaration>

<function-definition> ::= {<declaration-specifier>}* <declarator> {<declaration>}* <compound-statement>

<declaration-specifier> ::= <storage-class-specifier> | <type-specifier> | <type-qualifier>

<storage-class-specifier> ::= auto | register | static | extern | typedef

<type-specifier> ::= void | char | short | int | long | float | double | signed | unsigned | <struct-or-union-specifier> | <enum-specifier> | <typedef-name>

<struct-or-union-specifier> ::= <struct-or-union> <identifier> { {<struct-declaration>}+ } | <struct-or-union> { {<struct-declaration>}+ } | <struct-or-union> <identifier>

<struct-or-union> ::= struct | union

<struct-declaration> ::= {<specifier-qualifier>}* <struct-declarator-list>

<specifier-qualifier> ::= <type-specifier> | <type-qualifier>

<struct-declarator-list> ::= <struct-declarator> | <struct-declarator-list> , <struct-declarator>

<struct-declarator> ::= <declarator> | <declarator> : <constant-expression> | : <constant-expression>

<declarator> ::= {<pointer>}? <direct-declarator>

<pointer> ::= * {<type-qualifier>}* {<pointer>}?

<type-qualifier> ::= const | volatile

<direct-declarator> ::= <identifier> | ( <declarator> ) | <direct-declarator> [ {<constant-expression>}? ] | <direct-declarator> ( <parameter-type-list> ) | <direct-declarator> ( {<identifier>}* )

<constant-expression> ::= <conditional-expression>

<conditional-expression> ::= <logical-or-expression> | <logical-or-expression> ? <expression> : <conditional-expression>

<logical-or-expression> ::= <logical-and-expression> | <logical-or-expression> || <logical-and-expression>

<logical-and-expression> ::= <inclusive-or-expression> | <logical-and-expression> && <inclusive-or-expression>

<inclusive-or-expression> ::= <exclusive-or-expression> | <inclusive-or-expression> | <exclusive-or-expression>

<exclusive-or-expression> ::= <and-expression> | <exclusive-or-expression> ^ <and-expression>

<and-expression> ::= <equality-expression> | <and-expression> & <equality-expression>

<equality-expression> ::= <relational-expression> | <equality-expression> == <relational-expression> | <equality-expression> != <relational-expression>

<relational-expression> ::= <shift-expression> | <relational-expression> < <shift-expression> | <relational-expression> > <shift-expression> | <relational-expression> <= <shift-expression> | <relational-expression> >= <shift-expression>

<shift-expression> ::= <additive-expression> | <shift-expression> << <additive-expression> | <shift-expression> >> <additive-expression>

<additive-expression> ::= <multiplicative-expression> | <additive-expression> + <multiplicative-expression> | <additive-expression> - <multiplicative-expression>

<multiplicative-expression> ::= <cast-expression> | <multiplicative-expression> * <cast-expression> | <multiplicative-expression> / <cast-expression> | <multiplicative-expression> % <cast-expression>

<cast-expression> ::= <unary-expression> | ( <type-name> ) <cast-expression>

<unary-expression> ::= <postfix-expression> | ++ <unary-expression> | -- <unary-expression> | <unary-operator> <cast-expression> | sizeof <unary-expression> | sizeof <type-name>

<postfix-expression> ::= <primary-expression> | <postfix-expression> [ <expression> ] | <postfix-expression> ( {<assignment-expression>}* ) | <postfix-expression> . <identifier> | <postfix-expression> -> <identifier> | <postfix-expression> ++ | <postfix-expression> --

<primary-expression> ::= <identifier> | <constant> | <string> | ( <expression> )

<constant> ::= <integer-constant> | <character-constant> | <floating-constant> | <enumeration-constant>

<expression> ::= <assignment-expression> | <expression> , <assignment-expression>

<assignment-expression> ::= <conditional-expression> | <unary-expression> <assignment-operator> <assignment-expression>

<assignment-operator> ::= = | *= | /= | %= | += | -= | <<= | >>= | &= | ^= | |=

<unary-operator> ::= & | * | + | - | ~ | !

<type-name> ::= {<specifier-qualifier>}+ {<abstract-declarator>}?

<parameter-type-list> ::= <parameter-list> | <parameter-list> , ...

<parameter-list> ::= <parameter-declaration> | <parameter-list> , <parameter-declaration>

<parameter-declaration> ::= {<declaration-specifier>}+ <declarator> | {<declaration-specifier>}+ <abstract-declarator> | {<declaration-specifier>}+

<abstract-declarator> ::= <pointer> | <pointer> <direct-abstract-declarator> | <direct-abstract-declarator>

<direct-abstract-declarator> ::=  ( <abstract-declarator> ) | {<direct-abstract-declarator>}? [ {<constant-expression>}? ] | {<direct-abstract-declarator>}? ( {<parameter-type-list>}? )

<enum-specifier> ::= enum <identifier> { <enumerator-list> } | enum { <enumerator-list> } | enum <identifier>

<enumerator-list> ::= <enumerator> | <enumerator-list> , <enumerator>

<enumerator> ::= <identifier> | <identifier> = <constant-expression>

<typedef-name> ::= <identifier>

<declaration> ::=  {<declaration-specifier>}+ {<init-declarator>}* ;

<init-declarator> ::= <declarator> | <declarator> = <initializer>

<initializer> ::= <assignment-expression> | { <initializer-list> } | { <initializer-list> , }

<initializer-list> ::= <initializer> | <initializer-list> , <initializer>

<compound-statement> ::= { {<declaration>}* {<statement>}* }

<statement> ::= <labeled-statement> | <expression-statement> | <compound-statement> | <selection-statement> | <iteration-statement> | <jump-statement>

<labeled-statement> ::= <identifier> : <statement> | case <constant-expression> : <statement> | default : <statement>

<expression-statement> ::= {<expression>}? ;

<selection-statement> ::= if ( <expression> ) <statement> | if ( <expression> ) <statement> else <statement> | switch ( <expression> ) <statement>

<iteration-statement> ::= while ( <expression> ) <statement> | do <statement> while ( <expression> ) ; | for ( {<expression>}? ; {<expression>}? ; {<expression>}? ) <statement>

dict_bnf["jump-statement"] = r"goto <identifier> ; | continue ; | break ; | return {<expression>}? ;"

"""

