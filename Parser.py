import re
import sys

# this is the lexer right here that puts every valid token into a list
class Reading:

    tokens = list()

    class Comment(object):
        def __init__(self):
            self._x = None

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value

    def token(self, key, tokens):
        tokens.append((key, self))


    def tokenizer(self, token, tokens, comments):
        while self:
            self = self.strip()
            in_block = comments.x
            if in_block:
                while self:
                    if re.match('\\*/', self):
                        self = self[2:]
                        self = self.strip()
                        comments.x = False
                        break
                    else:
                        self = self[1:]
                        self = self.strip()
                        pass
            elif re.match('\\bint\\b|\\bwhile\\b|\\bvoid\\b|\\breturn\\b|\\belse\\b|\\bif\\b', self) and not in_block:
                key = re.match('int|while|void|return|else|if', self).group()
                token(key, 'KEYWORD:', tokens)
                self = self[len(key):]
                #print('KEYWORD: ' + key)
                pass
            elif re.match('[a-zA-Z]+', self) and not in_block:
                key = re.match('[a-zA-Z]+', self).group()
                token(key, 'ID:', tokens)
                self = self[len(key):]
                #print('ID: ' + key)
                pass
            elif re.match('[0-9]+', self) and not in_block:
                key = re.match('[0-9]+', self).group()
                token(key, 'NUM:', tokens)
                self = self[len(key):]
                #print('NUM: ' + key)
                pass
            elif re.match('[^\\s0-9a-zA-Z]+', self) and not in_block:
                key = re.match('[^\\s0-9a-zA-Z]+', self).group()
                if key.startswith(';') and not in_block:
                    token(key, 'TERMINATOR:', tokens)
                    self = self[len(key):]
                    #print('TERMINATOR: ' + key)
                elif re.match('//[\\s\\S]*?', self):
                    self = self[:0]
                elif re.match('/\\*[\\s\\S]*?\\*/', self) and not in_block:
                    comment = re.match('/\\*[\\s\\S]*?\\*/', self).group()
                    self = self[len(comment):]
                elif re.match('/\\*', self):
                    comments.x = True
                    break
                elif re.match('==|<=|>=|!=', key) and not in_block:
                    key = key[:2]
                    token(key, 'RELATION:', tokens)
                    self = self[len(key):]
                    #print('RELATION: ' + key)
                elif re.match('[*]|/|[+]|=|-|<|>|,|[(]|[)]|[{]|[}]|\\]|\\[', key) and not in_block:
                    key = key[:1]
                    token(key, 'OPERATION:', tokens)
                    self = self[len(key):]
                    #print('OPERATION: ' + key)
                    pass
                else:
                    key = re.match('[\\S]*', self).group()
                    key = key[:len(key)]
                    self = self[len(key):]
                    #print('ERROR: ' + key)
                    pass
    def remove(self, token, tokenizer, tokens, comments):
        is_comment = False
        for line in self:
            if line.strip() != '':
                 #print('INPUT:' + line.strip())
                pass
            if line.startswith('/*') or is_comment:
                is_comment = True
                line = line[2:]
                line = line.strip()
                while line:
                    if line.startswith('*/'):
                        line = line[2:]
                        line = line.strip()
                        is_comment = False
                        break
                    else:
                        line = line[1:]
                        line = line.strip()
                        pass
            tokenizer(line.strip(), token, tokens, comments)
    comments = Comment()

    file_name = sys.argv[1]
    try:
        with open(file_name, 'r') as f:
            remove(f, token, tokenizer, tokens, comments)
    except:
        print("FILE DOES NOT EXIST")

    f = open("write2.txt", "a+")
    for i in range(len(tokens)):
        f.write(tokens[i][0] + ' ' + tokens[i][1] + '\n')
    f.close()

###
###
###
###
###
###PARSER CLASS###

class Parser(object):
    x = -1
    def __init__(self, tokens):
        self.tokens = tokens
        if len(tokens)>0:
            self.current = self.tokens[self.count.getx()]
    class count:
        def __init__(self, x):
            self.x = x
        def getx(self):
            return self.x
        def setup(self, x):
            self.x += 1
        def setdown(self, x):
            self.x = x
        def setdown1(self, x):
            self.x -= x
    count = count(x)

    def error(self):
        print("REJECT")
        self.tokens.clear()
        f = open("write2.txt", "w")
        for i in range(len(self.tokens)):
            f.write(tokens[i][0] + ' ' + self.tokens[i][1] + '\n')
        f.close()
    def accept(self):
        print("ACCEPT")
        self.tokens.clear()
        f = open("write2.txt", "w")
        for i in range(len(self.tokens)):
            f.write(tokens[i][0] + ' ' + self.tokens[i][1] + '\n')
        f.close()

    def outrange(self):
        if self.count.getx() < len(self.tokens):
            return True
        else:
            return False

    """ program-->declaration-list """
    def program(self):
        #print(len(self.tokens))
        self.count.setup(self)
        if self.declaration_list():
            #print(self.count.getx())
            #print(len(self.tokens))
            if self.count.getx() == len(self.tokens):
                self.accept()
            else:
                self.error()
        else:
            self.error()

    """ declaration-list-->declaration declaration-list' """
    def declaration_list(self):
        #print("got into declaration list")
        if self.declaration():
            if self.declaration_list_2():
                return True
            else:
                return False
        else:
            return False
    """ declaration-list'-->declaration declaration-list' | empty """
    def declaration_list_2(self):
        #print("got into declaration list2")
        current = self.count.getx()
        if self.declaration():
            if self.declaration_list_2():
                return True
            else:
                self.count.setdown(current)
                return True
        else:
            self.count.setdown(current)
            return True
        #do fun declaration
    """ declaration-->var-declaration | fun-declaration """
    def declaration(self):
        current = self.count.getx()
        #print("Got in declaration")
        if self.var_declaration():
            return True

        elif self.fun_declaration():
            return True
        else:
            return False

    """ var-declaration-->type-specifier id ; | type-specifier id [ num ] ;"""
    def var_declaration(self):
        current = self.count.getx()
        #print("got into var declaration")
        if self.type_specifier():
            #print(self.tokens[self.count.getx()][0])
            if(self.tokens[self.count.getx()][0]) == "ID:":
                #print("this is an ID---------------------", self.tokens[self.count.getx()][1])
                self.count.setup(self)
                if(self.tokens[self.count.getx()][0]) == "TERMINATOR:":
                    #print("this is a TERMINATOR------------", self.tokens[self.count.getx()][1])
                    self.count.setup(self)
                    return True
                elif(self.tokens[self.count.getx()][1]) == "[":
                    #print("this is a START ARRAY-----------------", self.tokens[self.count.getx()][1])
                    self.count.setup(self)
                    if (self.tokens[self.count.getx()][0]) == "NUM:":
                        #print("this is a SIZE ARRAY----------------", self.tokens[self.count.getx()][1])
                        self.count.setup(self)
                        if (self.tokens[self.count.getx()][1]) == "]":
                            #print("this is a END ARRAY-----------------", self.tokens[self.count.getx()][1])
                            self.count.setup(self)
                            if (self.tokens[self.count.getx()][0]) == "TERMINATOR:":
                                #print("this is a TERMINATOR------------", self.tokens[self.count.getx()][1])
                                self.count.setup(self)
                                return True
                            else:
                                return False
                        else:
                            return False
                else:
                    self.count.setdown(current)
                    return False
        else:
            self.count.setdown(current)
            return False


    """ type-specifier-->int | void """
    def type_specifier(self):
        if self.count.getx() < len(self.tokens):
            #print("got into type specifier")
            if self.tokens[self.count.getx()][1] == "int":
                #print("this is the type specifier------------------", self.tokens[self.count.getx()][1])
                self.count.setup(self)
                return True
            elif self.tokens[self.count.getx()][1] == "void":
                #print("this is the type specifier--------------------", self.tokens[self.count.getx()][1])
                self.count.setup(self)
                return True
            else:
                return False
        else:
            return False
    """ fun-declaration--> type-specifier id ( params ) compound-stmt """
    def fun_declaration(self):
        #print("Got into fun declaration")
        if self.type_specifier():
            #print(self.tokens[self.count.getx()][0])

            if (self.tokens[self.count.getx()][0]) == "ID:":
                #print("this is an ID-------------------------", self.tokens[self.count.getx()][1])
                self.count.setup(self)

                if (self.tokens[self.count.getx()][1]) == "(":
                    #print("this is an OPEN PAREN------------------------", self.tokens[self.count.getx()][1])
                    self.count.setup(self)

                    if self.params():
                        #print("PASSED PARAMS")
                        #print(self.tokens[self.count.getx()][1])
                        if(self.tokens[self.count.getx()][1]) == ")":
                            #print("this is an CLOSE PAREN--------------------", self.tokens[self.count.getx()][1])
                            self.count.setup(self)
                            if self.compound_stmt():
                                #print("PASSED COMPOUND STMT")
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


    """ params-->param-list | void """
    def params(self):
        #print("Got Into PARAMS")

        if self.param_list():
            return True
        elif (self.tokens[self.count.getx()][1]) == "void":
            #print("this is a type SPECIFIER-------------------", self.tokens[self.count.getx()][1])
            self.count.setup(self)
            return True
        else:
            return False
    """ param-list-->, param param-list'"""
    def param_list(self):
        current = self.count.getx()
        #print("Got Into Param_List")
        if self.param():
            if self.param_list_2():
                return True
            else:
                self.count.setdown(current)
                return True
        else:
            self.count.setdown(current)
            return False
    """ param-list'-->, param param-list' | empty """
    def param_list_2(self):
        current = self.count.getx()
        if (self.tokens[self.count.getx()][1]) == ",":
            self.count.setup(self)
            if self.param():
                if self.param_list_2():
                    return True
                else:
                    self.count.setdown(current)
                    return True
            else:
                self.count.setdown(current)
                return True
        else:
            self.count.setdown(current)
            return True
    """ param--> type-specifier id | type-specifier id [ ] """
    def param(self):
        #print("GOT INTO PARAM")
        if self.type_specifier():
            current = self.count.getx()
            if (self.tokens[self.count.getx()][1]) == "void:" or (self.tokens[self.count.getx()][0]) == "ID:":
                self.count.setup(self)
                if (self.tokens[self.count.getx()][1]) == "[":
                    self.count.setup(self)
                    if (self.tokens[self.count.getx()][1]) == "]":
                        self.count.setup(self)
                        return True
                    else:
                        return False
                elif(self.tokens[current][1]) == "void:" or (self.tokens[current][0]) == "ID:":
                    self.count.setdown(current+1)
                    return True
            else:
                return False
        else:
            return False
    """ compound-stmt-->{ local-declarations statement-list } """
    def compound_stmt(self):
        if self.count.getx() < len(self.tokens):
            #print("Got into COMPOUND STMT")
            if self.outrange() and (self.tokens[self.count.getx()][1]) == "{":
                #print("this is an start COMPOUND", self.tokens[self.count.getx()][1])
                self.count.setup(self)
                if self.local_declarations():
                    #print("PASSED THRought declarations in COMPOUND STATMENET")
                    if self.statement_list():
                        #print("PASSED THROUGH STATEMENT_LIST IN COMPOUND STATEMENT")
                        if self.outrange() and (self.tokens[self.count.getx()][1]) == "}":
                            #print("this is an END COMPOUND1", self.tokens[self.count.getx()][1])
                            self.count.setup(self)
                            return True
                        else:
                            return False

                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    """ local-declarations-->local-declarations' """
    def local_declarations(self):
        if self.local_declaration_2():
            return True
        else:
            return False
    """ local-declarations'-->var-declaration local-declarations' | empty """
    def local_declaration_2(self):
        current = self.count.getx()
        #print("Got in declaration")
        if self.var_declaration():
            if self.local_declaration_2():
                return True
            else:
                self.count.setdown(current)
                return True
        else:
            self.count.setdown(current)
            return True
    """ statement-list'-->statement statment-list' | empty """
    def statement_list(self):
        current = self.count.getx()
        #print("got into STATEMENT LIST")
        if self.statement():
            if self.statement_list():
                return True
            else:
                self.count.setdown(current)
                return True
        else:
            self.count.setdown(current)
            return True
    """ statement-->expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt """
    def statement(self):
        #need to make current so if fails all the functions can update back the token index
        #print("Got into STATEMENT")
        if self.expression_stmt():
            #print("Going to EXPRESSION STMT")
            return True
        elif self.selection_stmt():
            #print("GOING TO SELECTION STMT")
            return True
        elif self.iteration_stmt():
            #print("GOINT TO ITERATION STMT")
            return True
        elif self.return_stmt():
            #print("GOING TO RETURN STMT")
            return True
        elif self.compound_stmt():
            #print("Going TO COMPOUND STMT")
            return True
        else:
            return False
    """ expression-stmt-->expression ; | ; """
    def expression_stmt(self):
        #print("got into EXPRESSION STMT")
        if self.count.getx() < len(self.tokens):
            current = self.count.getx()
            if self.expression():
                if(self.tokens[self.count.getx()][1]) == ";":
                    self.count.setup(self)
                    return True
                else:
                    self.count.setdown(current)
                    return False
            elif(self.tokens[self.count.getx()][0]) == "TERMINATOR:":
                self.count.setup(self)
                return True
            else:
                return False
        else:
            return False
    """ selection-stmt-->if ( expression ) statement | if ( expression ) statement else statement """
    def selection_stmt(self):
        if self.count.getx() < len(self.tokens):
            current = self.count.getx()
            #print("GOT INTO SELECTION")
            if (self.tokens[self.count.getx()][1]) == "if":
               #print("FOUND IF--------------", self.tokens[self.count.getx()][1])
                self.count.setup(self)
                if (self.tokens[self.count.getx()][1]) == "(":
                    #print("FOUND PAREN--------------", self.tokens[self.count.getx()][1])
                    self.count.setup(self)
                    if self.expression():
                        #print("GOT PAST EXPRESSION CONDITION GOOD")
                        if (self.tokens[self.count.getx()][1]) == ")":
                            self.count.setup(self)
                            if self.statement():
                                #print("got first statement when out of PARENS")
                                if (self.tokens[self.count.getx()][1]) == "else":
                                    #print(self.tokens[self.count.getx()][1])
                                    self.count.setup(self)
                                    if self.statement():
                                        return True
                                    else:
                                        return False
                                else:
                                    return True
                        else:
                            self.count.setdown(current)
                            return False
                    else:
                        self.count.setdown(current)
                        return False
                else:
                    self.count.setdown(current)
                    return False
        else:
            return False
    """ iteration-stmt-->while ( expression ) statement """
    def iteration_stmt(self):
        if self.count.getx() < len(self.tokens):
            #print("GOT INTO ITERATION")
            if (self.tokens[self.count.getx()][1]) == "while":
                self.count.setup(self)
                if (self.tokens[self.count.getx()][1]) == "(":
                    #print("FOUND PAREN--------------", self.tokens[self.count.getx()][1])
                    self.count.setup(self)
                    if self.expression():
                        if (self.tokens[self.count.getx()][1]) == ")":
                            self.count.setup(self)
                            if self.statement():
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    """ return-stmt--> return ; | return expression ; """
    def return_stmt(self):
        if self.count.getx() < len(self.tokens):
            #print("GOT INTO RETURN")
            if (self.tokens[self.count.getx()][1]) == "return":
                self.count.setup(self)
                if (self.tokens[self.count.getx()][0]) == "TERMINATOR:":
                    self.count.setup(self)
                    return True
                elif self.expression():
                    if (self.tokens[self.count.getx()][0]) == "TERMINATOR:":
                        self.count.setup(self)
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    """ expression-->var = expression | simple expression """
    def expression(self):
        if self.count.getx() < len(self.tokens):
            current = self.count.getx()
            #print("GOT INTO EXPRESSION")
            #print("ggyyyyyyyyyyyyyyyyyyyyyyy", self.tokens[self.count.getx()][1])
            if self.var():
                if (self.tokens[self.count.getx()][1]) == "=":
                    #print("ggggggggggggggggggggggggggggggg", self.tokens[self.count.getx()][1])
                    self.count.setup(self)
                    #print("ggggggggggggggggggggggggggggggg", self.tokens[self.count.getx()][1])
                    if self.expression():
                        #print("vvvvvvvvvvvvvvvvvvvvvvvvvvvv", self.tokens[self.count.getx()][1])
                        return True
                    else:
                        return False
                else:
                    self.count.setdown(current)
                    #print("..........................", self.tokens[current][1])

            if self.simple_expression():
                #print("ggggggggggggggggggggggggggggggg", self.tokens[self.count.getx()][1])
                #print("GOT BACK INTO SIMPLE EXPRESSION")
                return True
            else:

                return False
        else:
            return False
    """ var-->id | id [ expression ] """
    def var(self):
        #print("GOT INTO VAR")

        if (self.tokens[self.count.getx()][0]) == "ID:":
            current = self.count.getx()
            self.count.setup(self)
            if (self.tokens[self.count.getx()][1]) == "[":
                #print(self.tokens[self.count.getx()][1])
                self.count.setup(self)
                if self.expression():
                    if (self.tokens[self.count.getx()][1]) == "]":
                        self.count.setup(self)
                        return True
                    else:
                        self.count.setdown(current)
                        return False

            elif(self.tokens[current][0]) == "ID:":
                if(self.tokens[current+1][1]) != "(":
                    #print("THE ID IN THE VAR----------------", self.tokens[current][1])
                    current += 1
                    self.count.setdown(current)
                    return True
                else:
                    #print("tttttttttttttttttttt", self.tokens[current][1])
                    self.count.setdown(current)
                    return False
        else:

            return False
    """ simple-expression--> additive-expression relop additive-expression | additive-expression """
    def simple_expression(self):
        #print("GOT INTO SIMPLE EXPRESSION")
        #print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn", self.tokens[self.count.getx()][1])
        current = self.count.getx()
        if self.additive_expression():
            if self.relop():
                if self.additive_expression():
                    return True
                else:
                    self.count.setdown(current)
                    return False
            else:
                self.count.setdown(current)
                self.count.setdown(current)
        if self.additive_expression():
            return True
        else:
            return False
    """ relop--> <= | < | > | >= | == | != """
    def relop(self):
        #print("GOT INTO RELOP")
        if (self.tokens[self.count.getx()][1]) == "<=":
            self.count.setup(self)
            return True
        elif (self.tokens[self.count.getx()][1]) == ">=":
            self.count.setup(self)
            return True
        elif (self.tokens[self.count.getx()][1]) == ">":
            self.count.setup(self)
            return True
        elif (self.tokens[self.count.getx()][1]) == "<":
            self.count.setup(self)
            return True
        elif (self.tokens[self.count.getx()][1]) == "==":
            self.count.setup(self)
            return True
        elif (self.tokens[self.count.getx()][1]) == "!=":
            self.count.setup(self)
            return True
        else:
            return False
    """ additive-expression--> term additive-expression' """
    def additive_expression(self):
        #print("GOT INTO ADDITIVE EXPRESION")
        #print("kkkkkkkkkkkkkkkkkkkkkkkk", self.tokens[self.count.getx()][1])
        if self.term():
            if self.additive_expression_2():
                return True
            else:
                return False
        else:
            return False
    """ additive-expression'--> addop term additive-expression' | empty """
    def additive_expression_2(self):
        current = self.count.getx()
        #print("Got into additive expression2")
        if self.addop():
            if self.term():
                if self.additive_expression_2():
                    return True
                else:
                    self.count.setdown(current)
                    return True
            else:
                self.count.setdown(current)
                return True
        else:
            self.count.setdown(current)
            #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa", self.tokens[self.count.getx()][1])
            return True
    """ addop--> + | - """
    def addop(self):
        #print("GOT INTO ADDOP")
        if (self.tokens[self.count.getx()][1]) == "+":
            self.count.setup(self)
            return True
        elif (self.tokens[self.count.getx()][1]) == "-":
            self.count.setup(self)
            return True
        else:
            return False
    """ term--> factor term' """
    def term(self):
        #print("GOT INTO TERM")
        #print("kkkkkkkkkkkkkkkkkkkkkkkk", self.tokens[self.count.getx()][1])
        if self.factor():
            if self.term_2():
                return True
            else:
                return False
        else:
            return False
    """ term'--> mulop factor term' | empty """
    def term_2(self):
        current = self.count.getx()
        #print("GOT INTO TERM 2")
        if self.mulop():
            if self.factor():
                if self.term_2():
                    return True
                else:
                    self.count.setdown(current)
                    return True
            else:
                self.count.setdown(current)
                return True
        else:
            self.count.setdown(current)
            #print("kkkkkkkkkkkkkkkkkkkkkkkk", self.tokens[self.count.getx()][1])
            return True
    """ mulop--> * | / """
    def mulop(self):
        #print("GOT INTO MULOP")
        if (self.tokens[self.count.getx()][1]) == "*":
            self.count.setup(self)
            return True
        elif(self.tokens[self.count.getx()][1]) == "/":
            self.count.setup(self)
            return True
        else:
            return False
    """ factor-->( expression ) | call | var | num """
    def factor(self):
        #print("GOT INTO FACTOR")
        #print("ffffffffffffffffffffffffffffffffff", self.tokens[self.count.getx()][1])
        if (self.tokens[self.count.getx()][1]) == "(":
            #print("FOUND PAREN--------------", self.tokens[self.count.getx()][1])
            self.count.setup(self)
            if self.expression():
                if (self.tokens[self.count.getx()][1]) == ")":
                    self.count.setup(self)
                    return True
                else:
                    return False
            else:
                return False
        elif self.call():
            return True
        elif self.var():
            return True
        elif(self.tokens[self.count.getx()][0]) == "NUM:":
            #print("kkkmmmmmmmmmmmmmmmmmmmmmmm", self.tokens[self.count.getx()][1])
            self.count.setup(self)
            #print("kkkkkkkkkkkkkkkkkkkkkkkk", self.tokens[self.count.getx()][1])
            return True
        else:
            return False
    """ call-->id ( args ) """
    def call(self):
        current = self.count.getx()
        #print("GOT INTO CALL")
        if (self.tokens[self.count.getx()][0]) == "ID:":
            #print("THE ID IN THE CALL----------------", self.tokens[self.count.getx()][1])
            self.count.setup(self)
            if (self.tokens[self.count.getx()][1]) == "(":
                self.count.setup(self)
                if self.args():
                    if (self.tokens[self.count.getx()][1]) == ")":
                        self.count.setup(self)
                        return True
                    else:
                        #
                        #
                        self.count.setdown(current)
                        return False
                else:
                    #
                    #
                    self.count.setdown(current)
                    return False
            else:
                #print("=============================", self.tokens[current][1])
                self.count.setdown(current)
                return False
        else:
            return False

    """ args--> arg-list | empty """
    def args(self):
        #print("GOT INTO ARGS")
        if self.arg_list():
            return True
        else:
            return True
    """ arg-list--> expression arg-list' """
    def arg_list(self):
        #print("GOT INTO ARGLIST")
        #print("////////////////////////////////////////", self.tokens[self.count.getx()][1])
        if self.expression():
            if self.arg_list_2():
                return True
        else:
            return False
    """ arg-list'-->, expression arg-list' | empty """
    def arg_list_2(self):

        current = self.count.getx()
        #print("GOT INTO ARGLIST 2")
        if (self.tokens[self.count.getx()][1]) == ",":
            self.count.setup(self)
            if self.expression():
                if self.arg_list_2():
                    return True

            else:
                self.count.setdown(current)
                return False
        else:
            self.count.setdown(current)
            return True
tokens = list()
f = open("write2.txt", "r")
lines = f.readlines()
for line in lines:
    key = re.match('[\\s\\S]*:', line).group()
    line = line[len(key):].strip()
    tokens.append((key, line))
f.close()
#print(tokens)
if len(tokens) > 0:
    parse = Parser(tokens)
    parse.program()
else:
    parse = Parser(tokens)
    parse.error()

