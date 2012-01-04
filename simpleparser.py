# Simple Parser for a simple language called GUTS
# (if it even qualifies as 'language').
# Created by Craig McL <mistercouk@gmail.com> on 6/12/2011
# Last edited on 4/1/2012 by Craig McL <mistercouk@gmail.com>
# EBNF Grammar defined below for GUTS.
#
# Note there is alot of 'filler' nonterminal symbols
# defined here that are not implemented in the parser
# below to allow the language to expand if/when
# appropriate.
#
# Terminals are enclosed in single quotes.
# Non-Terminals are captialised.
#
# Note for brevity some of the expression used here
# are not 'standard' EBNF but more commonly found in
# regular expression e.g use of [A-Za-z] to denote a class
# of characters is used instead of individually specifying
# each character or [^"] to denote anything but a double
# quotation.
#
##########################################################
#
#   Program         ::= Smt
#                   |   '`' ('-')? Expression
#
#   Smt             ::= 'print' StringLiteral
#                   |   'var' Identifier '=' Expression
#                   |   'create' Access NameSpace
#                   |   'use' NameSpace
#                   |   'share' NameSpace 'with' User
#                   |   'ns'
#
#
#   Expression      ::= Term (AdOp Term)*
#
#   Term            ::= Factor (MulOp Factor)*
#
#   Factor          ::= Number ('^' Number)*
#
#   Number          ::= IntLiteral
#                   |   FloatLiteral
#                   |   '(' Expression ')'
#                   |   Identifier
#
#   AdOp            ::= '+' | '-'
#
#   MulOp           ::= '*'
#                   |   '/'
#                   |   '^'
#
#   StringLiteral   ::= '"' '[^"]' '"'
#
#   IntLiteral      ::= '([0-9])*'
#
#   FloatLiteral    ::= '([0-9])*' '.' '([0-9])*'
#
#   Access          ::= 'public'
#                   |   'private'
#
#   NameSpace       ::= Identifier
#
#   User            ::= Identifer
#
#

import re
from contextanalyser import *

# Test class
class b(object):
    def send(self, string):
        print string

class SimpleSyntaxError(Exception):
    """Syntax Error Exception class."""
    def __init__(self, sp, token):
        self.spelling = sp
        if Token.toks.get(token, None):
            self.token = Token.toks[token]
        else:
            self.token = token

    def __repr__(self):
        return "SimpleSyntaxError()"

    def __str__(self):
        return "Syntax Error with '{}'; expected '{}'".format(
            self.spelling, self.token)

class Token(object):
    """Defines the tokens recognised by the parser."""
    # Quick access to punctuation literals
    punct = ["(", ")", "*", "+", "/", "-", "^", "`", "="]
    # Some keywords
    keywords = ["PRINT", "VAR", "CREATE", "PUBLIC", "PRIVATE",
                "USE", "WITH", "SHARE", "NS"]
    # Map tokens to spelling
    toks = {"NUMBER" : "<NUMBER>", "IDENT" : "<IDENT>", "PRINT" : "print",
            "LPAREN" : "(", "RPAREN" : ")", "MUL" : "*", "QUOTE" : "\"",
            "ADD" : "+", "DIV" : "/", "SUB" : "-", "ASSIGN" : "=",
            "POW" : "^", "ERROR" : "error", "VAR" : "var",
            "EOT" : "end-of-text", "BACKTICK" : "`", "CREATE" : "create",
            "PUBLIC" : "public", "PRIVATE" : "private",
            "USE" : "use", "WITH" : "with", "SHARE" : "share", "NS" : "ns",
            "STRING_LITERAL" : "[^\"]"}
    def __init__(self, sp, tok):
        """Creates a Token instance.

        Performs some processing on the values received:
            * if sp and tok are both None we safeguard against that by
              sticking error string in both.
            * if the spelling matches a keyword the token is changed
              to match the type of token for the keyword.
            * if the spelling matches one of our punctuation symbols
              the token is changed to the token type corresponding to the
              punctuation symbol.
            * otherwise we just store the spelling and token type.
        """
        if sp is None and tok is None:
            sp = "ERROR"
            tok = "ERROR"
        elif sp.upper() in Token.keywords:
            tok = sp.upper()
        elif sp.upper() in Token.punct:
            for k, v in Token.toks.iteritems():
                if sp == v:
                    tok = k
                    break
                
        self.sp = sp
        self.type = tok

    def get_spelling(self):
        """Returns the spelling of the token."""
        return self.sp

    def is_type(self, tokType):
        """Compares the type of this token with tokType.

        if tokType isn't a valid type it returns false otherwise
        the method returns the type of the comparison.
        """
        if Token.toks.get(tokType, None):
            return self.type == tokType
        return False

    def get_type(self):
        """Returns the type of this token."""
        return self.type

class Lexer(object):
    """Lexical Analyser for the small language being implemented here.

    Scans the string passed into the constructor one character at a time.
    """

    def __init__(self, string):
        string = string.strip()
        # Get a generator object for the string of chars
        self.stream = self.gen(string)
        # Load the first character from the stream
        self.get_char()
        
    def gen(self, string):
        """Method that returns a char generator to the string stream."""
        for c in string:
            yield c

    def get_char(self):
        """Get the next character from the stream."""
        try:
            self.char = self.stream.next()
        except StopIteration as e:
            self.char = "-1"

    def isdigit(self, char):
        """Returns boolean value: True if char is a digit, False otherwise."""
        return char >= '0' and char <= '9'

    def isalpha(self, char):
        """Returns boolean value: True if char is a alpha, False otherwise."""
        return ((char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'))

    def scan_sep(self):
        """Method to get rid of whitespace from the stream."""
        while self.char.isspace():
            self.get_char()

    def get_num(self):
        """Method to extract the digits of a number from the stream."""
        n = ""
        while self.isdigit(self.char):
            n = n + self.char
            self.get_char()
        return n

    def get_quoted_string(self):
        """Method to extract the letters of a string literal from the stream."""
        n = ""
        while re.match(Token.toks["STRING_LITERAL"] + "$", self.char):
            n = n + self.char
            self.get_char()
        return n
    
    def get_next(self):
        """Method to return the next Token object in the stream."""
        if self.char is None:
            return Token(None, None)

        self.scan_sep()
        
        if self.isdigit(self.char):
            n = self.get_num()
            # Check for floating point notation
            if self.char == ".":
                self.get_char() # Get the next number
                afterPoint = self.get_num()
                # if it's just a dot and no numbers after it
                # append a zero.
                if afterPoint == "":
                    n = n + "." + "0"
                else:
                    n = n + "." + afterPoint
            
            return Token(n, "NUMBER")
        elif self.isalpha(self.char):
            n = self.char
            self.get_char()
            # Identifier is only allowed be to alphabet characters
            while self.isalpha(self.char):
                n = n + self.char
                self.get_char()
            return Token(n, "IDENT")
        elif self.char == "\"":
            self.get_char()
            n = self.get_quoted_string()
            if self.char == "\"":
                self.get_char() # Accept closing quotation
                return Token(n, "STRING_LITERAL")
            else:
                return Token(self.char, "ERROR")
        elif self.char in Token.punct:
            # The same actions performed for all punctuation symbols
            n = self.char
            self.get_char()
            # Pass None as Token type; this is
            # dealt with by the Token class
            return Token(n, None)
        elif self.char == "-1":
            # End Of Text reached
            return Token("EOT", "EOT")
        else:
            # Error
            return Token(self.char, "ERROR")

class SimpleParser(object):
    """Recursive descent parser for the simple grammar being implemented here.

    Accepts a 'bot' (this is primarily for use with the gucs-bot but
    a wrapper class can be put over the usual printing facilities provided
    by an environment.

    If you want to use this class but not with a Bot object, then create
    a class with a 'send' method that takes one argument (a str object).

    The grammar this parser parses is defined at the top of this module for
    accessibility.

    The constructor takes no arguments and doesn't do anything. The main
    initialisation is performed in the parse method which takes the 'bot'
    and the str object to be parsed.
    """
    def __init__(self, contextAnalyser):
        """Stores the ContextAnalyser object passed in for later use.

        
        """
        self.context = contextAnalyser
        
    def accept(self, tok):
        """Checks that the type of the next token in the stream is tok.

        The method compares tok with the current token in the input stream
        if they are the same the next token in the stream is fetched otherwise
        a SimpleSyntaxError is thrown.
        """
        # Make sure token attribute is defined on this object.
        if hasattr(self, "token"):
            if self.token.is_type(tok):
                self.token = self.lexer.get_next()
            else:
                raise SimpleSyntaxError(self.token.get_spelling(), tok)
                
    def accept_tok(self):
        """Unconditionally accept the current token.

        Fetches the next token in the stream.
        """
        if hasattr(self, "token"):
            self.token = self.lexer.get_next()
        
    def parse(self, bot, string, user):
        """Initialises the resources and starts the parsing of string.

        user is the name of the user that sent the string to be executed
        we need to record this name for later use with the context analyser.
        """
        self.bot = bot
        self.user = user
        self.lexer = Lexer(string)
        self.token = self.lexer.get_next()
        self.parse_program()

    def parse_program(self):
        """Parse a program in accordance with the grammar."""
        try:
            if self.token.is_type("BACKTICK"):
                self.accept_tok()
                self.bot.send(">> {}".format(self.parse_cal()))
            else:
                self.parse_smt()
        except SimpleSyntaxError as e:
             self.bot.send("{}".format(e))
        except ContextError as e:
             self.bot.send("{}".format(e))

    def parse_smt(self):
        """Parse a statement in accordance with the grammar rules."""
        if self.token.is_type("PRINT"):
            self.accept_tok()
            self.parse_print()
        elif self.token.is_type("VAR"):
            self.accept_tok()
            # Add the variable to the namespace with a placeholder
            name = self.token.get_spelling()
            self.accept_tok() # Accept the identifer
            self.accept("ASSIGN")
            # Parse the expression and place the result in the variable
            self.context.add_ident(self.user, name, self.parse_cal())
        elif self.token.is_type("CREATE"):
            self.accept_tok()
            access = self.parse_access()
            # Create namespace using context analyser
            name = self.token.get_spelling()
            self.accept_tok()
            self.context.create_ns(name, self.user, access)
        elif self.token.is_type("USE"):
            self.accept_tok()
            # Use namespace using context analyser
            if self.token.is_type("IDENT"):
                try:
                    self.context.change_ns(self.user,
                                           self.token.get_spelling())
                except ContextError as e:
                    self.bot.send("{}".format(e))
            self.accept_tok() # Accept namespace name
        elif self.token.is_type("SHARE"):
            self.accept_tok()
            ns = self.token.get_spelling()
            self.accept_tok()
            self.accept("WITH")
            username = self.token.get_spelling()
            self.accept_tok()
            # Add user to namespace user list using context analyser
            try:
                self.context.share_ns(self.user, username, ns)
            except ContextError as e:
                self.bot.send("{}".format(e))
        elif self.token.is_type("NS"):
            self.accept_tok()
            self.bot.send(">> {}".format(self.context.get_ns_name(self.user)))
        else:
            raise SimpleSyntaxError(self.token.get_spelling(), "STATEMENT")

    def parse_print(self):
        """Parses a print statement."""
        self.bot.send(">> {}".format(self.parse_string_literal()))

    def parse_cal(self):
        """Parses a calculation.

        This is really just implicit in the grammar as an expression
        but the code is separated so as not to bloat the expr method.
        """
        expr = self.parse_expr()
        if not self.token.is_type("EOT"):
            raise SimpleSyntaxError(self.token.get_spelling(), "<OPERATOR>")
        return expr
    
    def parse_expr(self):
        """Parses an expression."""
        # Support for unary minus symbol
        if self.token.is_type("SUB"):
            self.accept_tok()
            term = - self.parse_term()
        else:
            term = self.parse_term()
        while (self.token.is_type("ADD") or
               self.token.is_type("SUB")):
            if self.token.is_type("ADD"):
                self.accept_tok()
                term = term + self.parse_term()
            elif self.token.is_type("SUB"):
                self.accept_tok()
                term = term - self.parse_term()
        return term

    def parse_term(self):
        """Parses a term."""
        factor = self.parse_factor()
        tokType = self.token.get_type()
        while tokType == "MUL" or tokType == "DIV":
            self.accept_tok()
            if tokType == "MUL":
                factor *= self.parse_factor()
            elif tokType == "DIV":
                try:
                    factor /= self.parse_factor()
                except ZeroDivisionError as e:
                    raise SimpleSyntaxError("0' in '{}/{}".format(factor, 0),
                                            "Non-zero number")
            tokType = self.token.get_type()
        return factor

    def parse_factor(self):
        """Parses a factor."""
        number = self.parse_number()
        while self.token.is_type("POW"):
            self.accept_tok()
            number **= self.parse_number()
        return number
            
    def parse_number(self):
        """Parses a number."""
        sp = self.token.get_spelling()
        # Number is an expression if enclosed in parentheses.
        if self.token.is_type("LPAREN"):
            self.accept_tok()
            expr = self.parse_expr()
            self.accept("RPAREN")
            return expr
        elif self.token.is_type("IDENT"):
            ident = self.token.get_spelling()
            try:
                value = self.context.get_ident(self.user, ident)
            except ContextError as e:
                raise
            else:
                return value
            finally:
                self.accept_tok()
        
        try:
            if sp.isdigit():
                number = int(sp)
            else:
                number = float(sp)
        except ValueError as e:
            raise SimpleSyntaxError(sp, "NUMBER")
        # Accept the number
        self.accept_tok()
        return number

    def parse_string_literal(self):
        """Parses a string literal."""
        # Should have a string literal token to parse
        # just simply return to caller.
        if self.token.is_type("STRING_LITERAL"):
            return self.token.get_spelling()
        else:
            raise SimpleSyntaxError(self.token.get_spelling(),
                                    "STRING_LITERAL")

    def parse_access(self):
        """Parses the access modifier."""
        if self.token.is_type("PUBLIC"):
            self.accept_tok()
            return True
        elif self.token.is_type("PRIVATE"):
            self.accept_tok()
            return False
        else:
            raise SimpleSyntaxError(self.token.get_spelling(),
                                    "Access Modifier")
