import re
import bnfparsing

def classify_bnf():
    with open("bnf_text.txt", "r", encoding="utf8") as fr:
        all_text = fr.readlines()
        all_text = [str(text).replace("\n", "") for text in all_text]

        all_text_classify = []
        for text in all_text:
            temp_text = str(text).strip(" ")

            if temp_text == "":
                continue

            if temp_text.startswith("|"):
                all_text_classify[-1] += " " + temp_text
            else:
                all_text_classify.append(temp_text)

        with open("bnf_classify.txt" , "w") as fw:
            fw.truncate()
            all_text_classify.reverse()

            pattern = r"(<(\w*-*)*>)"
            master_pat = re.compile(pattern)

            for full_text in all_text_classify:
                key = str(full_text.split("::=")[0]).strip()
                text = full_text.split("::=")[1]
                element = []

                ele_find = re.findall(master_pat, text)

                for ele in ele_find:
                    text = text.replace(ele[0], "\"ele\"")
                    element.append(ele[0])

                text = text.split("\"ele\"")
                text = [str(i).replace(" ", "") for i in text]

                text = ["\"" + str(word).replace("|", "\" | \"") + "\"" for word in text]
                index = 1

                for ele in element:
                    text.insert(index, " " + str(ele) + " ")
                    index += 2

                text = key + " := " + str("".join(text)).replace("\"\"","")
                fw.write(str(text)+"\n\n")


if __name__ == "__main__":
    classify_bnf()
#
    IF_STMT = """
<jump-statement> := "goto" <identifier> ";" | "continue;" | "break;" | "return{" <expression> "}?;"

<iteration-statement> := "while(" <expression> ")" <statement>  | "do" <statement> "while(" <expression> ");" | "for({" <expression> "}?;{" <expression> "}?;{" <expression> "}?)" <statement>

<selection-statement> := "if(" <expression> ")" <statement>  | "if(" <expression> ")" <statement> "else" <statement>  | "switch(" <expression> ")" <statement>

<expression-statement> := "{" <expression> "}?;"

<labeled-statement> :=  <identifier> ":" <statement>  | "case" <constant-expression> ":" <statement>  | "default:" <statement>

<statement> :=  <labeled-statement>  |  <expression-statement>  |  <compound-statement>  |  <selection-statement>  |  <iteration-statement>  |  <jump-statement>

<compound-statement> := "{{" <declaration> "}*{" <statement> "}*}"

<initializer-list> :=  <initializer>  |  <initializer-list> "," <initializer>

<initializer> :=  <assignment-expression>  | "{" <initializer-list> "}" | "{" <initializer-list> ",}"

<init-declarator> :=  <declarator>  |  <declarator> "=" <initializer>

<declaration> := "{" <declaration-specifier> "}+{" <init-declarator> "}*;"

<typedef-name> :=  <identifier>

<enumerator> :=  <identifier>  |  <identifier> "=" <constant-expression>

<enumerator-list> :=  <enumerator>  |  <enumerator-list> "," <enumerator>

<enum-specifier> := "enum" <identifier> "{" <enumerator-list> "}" | "enum{" <enumerator-list> "}" | "enum" <identifier>

<direct-abstract-declarator> := "(" <abstract-declarator> ")" | "{" <direct-abstract-declarator> "}?[{" <constant-expression> "}?]" | "{" <direct-abstract-declarator> "}?({" <parameter-type-list> "}?)"

<abstract-declarator> :=  <pointer>  |  <pointer>  <direct-abstract-declarator>  |  <direct-abstract-declarator>

<parameter-declaration> := "{" <declaration-specifier> "}+" <declarator>  | "{" <declaration-specifier> "}+" <abstract-declarator>  | "{" <declaration-specifier> "}+"

<parameter-list> :=  <parameter-declaration>  |  <parameter-list> "," <parameter-declaration>

<parameter-type-list> :=  <parameter-list>  |  <parameter-list> ",..."

<type-name> := "{" <specifier-qualifier> "}+{" <abstract-declarator> "}?"

<unary-operator> := "&" | "*" | "+" | "-" | "~" | "!"

<assignment-operator> := "=" | "*=" | "/=" | "%=" | "+=" | "-=" | "<<=" | ">>=" | "&=" | "^=" |  | "="

<assignment-expression> :=  <conditional-expression>  |  <unary-expression>  <assignment-operator>  <assignment-expression>

<expression> :=  <assignment-expression>  |  <expression> "," <assignment-expression>

<constant> :=  <integer-constant>  |  <character-constant>  |  <floating-constant>  |  <enumeration-constant>

<primary-expression> :=  <identifier>  |  <constant>  |  <string>  | "(" <expression> ")"

<postfix-expression> :=  <primary-expression>  |  <postfix-expression> "[" <expression> "]" |  <postfix-expression> "({" <assignment-expression> "}*)" |  <postfix-expression> "." <identifier>  |  <postfix-expression> "->" <identifier>  |  <postfix-expression> "++" |  <postfix-expression> "--"

<unary-expression> :=  <postfix-expression>  | "++" <unary-expression>  | "--" <unary-expression>  |  <unary-operator>  <cast-expression>  | "sizeof" <unary-expression>  | "sizeof" <type-name>

<cast-expression> :=  <unary-expression>  | "(" <type-name> ")" <cast-expression>

<multiplicative-expression> :=  <cast-expression>  |  <multiplicative-expression> "*" <cast-expression>  |  <multiplicative-expression> "/" <cast-expression>  |  <multiplicative-expression> "%" <cast-expression>

<additive-expression> :=  <multiplicative-expression>  |  <additive-expression> "+" <multiplicative-expression>  |  <additive-expression> "-" <multiplicative-expression>

<shift-expression> :=  <additive-expression>  |  <shift-expression> "<<" <additive-expression>  |  <shift-expression> ">>" <additive-expression>

<relational-expression> :=  <shift-expression>  |  <relational-expression> "<" <shift-expression>  |  <relational-expression> ">" <shift-expression>  |  <relational-expression> "<=" <shift-expression>  |  <relational-expression> ">=" <shift-expression>

<equality-expression> :=  <relational-expression>  |  <equality-expression> "==" <relational-expression>  |  <equality-expression> "!=" <relational-expression>

<and-expression> :=  <equality-expression>  |  <and-expression> "&" <equality-expression>

<exclusive-or-expression> :=  <and-expression>  |  <exclusive-or-expression> "^" <and-expression>

<inclusive-or-expression> :=  <exclusive-or-expression>  |  <inclusive-or-expression>  |  <exclusive-or-expression>

<logical-and-expression> :=  <inclusive-or-expression>  |  <logical-and-expression> "&&" <inclusive-or-expression>

<logical-or-expression> :=  <logical-and-expression>  |  <logical-or-expression>  |  |  <logical-and-expression>

<conditional-expression> :=  <logical-or-expression>  |  <logical-or-expression> "?" <expression> ":" <conditional-expression>

<constant-expression> :=  <conditional-expression>

<direct-declarator> :=  <identifier>  | "(" <declarator> ")" |  <direct-declarator> "[{" <constant-expression> "}?]" |  <direct-declarator> "(" <parameter-type-list> ")" |  <direct-declarator> "({" <identifier> "}*)"

<type-qualifier> := "const" | "volatile"

<pointer> := "*{" <type-qualifier> "}*{" <pointer> "}?"

<declarator> := "{" <pointer> "}?" <direct-declarator>

<struct-declarator> :=  <declarator>  |  <declarator> ":" <constant-expression>  | ":" <constant-expression>

<struct-declarator-list> :=  <struct-declarator>  |  <struct-declarator-list> "," <struct-declarator>

<specifier-qualifier> :=  <type-specifier>  |  <type-qualifier>

<struct-declaration> := "{" <specifier-qualifier> "}*" <struct-declarator-list>

<struct-or-union> := "struct" | "union"

<struct-or-union-specifier> :=  <struct-or-union>  <identifier> "{{" <struct-declaration> "}+}" |  <struct-or-union> "{{" <struct-declaration> "}+}" |  <struct-or-union>  <identifier>

<type-specifier> := "void" | "char" | "short" | "int" | "long" | "float" | "double" | "signed" | "unsigned" |  <struct-or-union-specifier>  |  <enum-specifier>  |  <typedef-name>

<storage-class-specifier> := "auto" | "register" | "static" | "extern" | "typedef"

<declaration-specifier> :=  <storage-class-specifier>  |  <type-specifier>  |  <type-qualifier>

<function-definition> := "{" <declaration-specifier> "}*" <declarator> "{" <declaration> "}*" <compound-statement>

<external-declaration> :=  <function-definition>  |  <declaration>

<translation-unit> := "{" <external-declaration> "}*"

<identifier> := "u"

    """


class IfStmtParser(bnfparsing.ParserBase):
    def __init__(self):
        super().__init__(ws_handler=bnfparsing.ignore)
        self.grammar(IF_STMT)

p = IfStmtParser()


