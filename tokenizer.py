class Token():
    def __init__(self, type: str, token: str, value):
        self.type = type
        self.token = token
        self.value = value

# ============ LEXER ============

def tokenize(source: str) -> list[Token]:
    # ======== OPERATORS ========
    OPERATORS = {
        # ==== ARTIHMETIC =======
        "TOKEN_PLUS": '+', # ADDITION
        "TOKEN_MINUS": '-', # SUBTRACTION
        "TOKEN_TIMES": '*', # MULTIPLICATION
        "TOKEN_DIV": '/', # DIVISION
        "TOKEN_MOD": '%', # MODULUS

        # ==== ASSIGNMENT =======
        "TOKEN_ASSIGN": '=',

        # ==== MISC =============
        "TOKEN_RETTYPE": "^"
    }

    # ======== COMPARISON =======
    COMPARES = {
        "TOKEN_EQ": "==",
        "TOKEN_LT": "<",
        "TOKEN_GT": ">",
        "TOKEN_LTEQ": "<=",
        "TOKEN_GTEQ": ">=",
        "TOKEN_NEQ": "!=",
        "TOKEN_AND": "&&",
        "TOKEN_OR": "||",
        "TOKEN_NOT": "!",
        "TOKEN_PARAMS": "->"
    }

    # ======== TYPE ============
    TYPE = {
        "TOKEN_INT": "int",
        "TOKEN_CHAR": "char",
        "TOKEN_STR": "string",
        "TOKEN_BOOL": "bool",
        "TOKEN_FLOAT": "float",
        "TOKEN_DICT": "dict",
        "TOKEN_INFER": "var",
        "TOKEN_VOID": "void"
    }

    # ======== MISC CHARACTERS ==
    CHARACTERS = {
        "TOKEN_SEMI": ";"
    }

    # ======== PUNCTUATION ======
    PUNCTUATION = {
        "TOKEN_LPAREN": "(",
        "TOKEN_RPAREN": ")",
        "TOKEN_LBRACE": "{",
        "TOKEN_RBRACE": "}",
        "TOKEN_LSQUARE": "[",
        "TOKEN_RSQUARE": "]",
        "TOKEN_COMMA": ",",
        "TOKEN_DOT": ".",
        "TOKEN_BACKSLASH": "\\"
    }

    # ======== KEYWORDS =========
    KEYWORDS = {
        "TOKEN_IF": "if",
        "TOKEN_OTHER": "other",
        "TOKEN_WHILE": "while",
        "TOKEN_FOR": "for",
        "TOKEN_IN": "in",
        "TOKEN_RET": "return",
        "TOKEN_DEF": "define",
        "TOKEN_STOP": "stop",
        "TOKEN_CONT": "continue",
        "TOKEN_GET": "get",
        "TOKEN_NULL": "null",
        "TOKEN_TRUE": "true",
        "TOKEN_FALSE": "false"
    }

    # ======== ALPHANUMERIC CHARS
    ALPHANUMERIC = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
        '_'
    ]

    # ======== NUMBERS ==========
    NUMBERS_WDOT = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'
    ]

    NUMBERS = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'
    ]

    ALPHA = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
        '_'
    ]

    # ======== DISALLOWED IN ID =
    DISALLOW = [
        '[', ']', '{', '}', '\\', '|', '`', 
        '~', '@', ',#', '$', '^', '&', 
        '(', ')', ',', '.', '?', ';', ' ', '\n'
    ]

    with open(source, "r") as f:
        content = f.read()
        tokens = []
        i = 0
        while i < len(content):
            if i + 1 >= len(content): next_char_eof = True
            else: next_char_eof = False
            c = content[i]
            pre_addition_tok_list = tokens.copy()
            if isinstance(c, str):
                if not next_char_eof and c == "\n":
                    tokens.append(Token(type="MISC", token="TOKEN_NEWLINE", value=c))
                    i += 1
                    continue
                elif c == "\\":
                    tokens.append(Token(type="PUNCTUATION", token="TOKEN_BACKSL", value=c))
                    i += 1
                    continue
                for token, v in OPERATORS.items():
                    if c == v:
                        if not next_char_eof:
                            if v == '=' and content[i + 1] == '=':
                                tokens.append(Token(type="COMPARES", token="TOKEN_EQ", value=v + content[i + 1]))
                                i += len(v + content[i + 1]);
                                break
                            elif v == '-' and content[i + 1] == '>':
                                tokens.append(Token(type="COMPARES", token="TOKEN_PARAMS", value=v + content[i + 1]))
                                i += len(v + content[i + 1])
                                break
                            else:
                                tokens.append(Token(type="OPERATOR", token=token, value=v))
                                i += 1
                                break
                        else: break
                if tokens != pre_addition_tok_list:
                    continue
                for token, v in COMPARES.items():
                    if not next_char_eof: 
                        next_char = content[i + 1]
                    else: 
                        next_char = None
                    if next_char != None and c == v[0]:
                        if next_char == v[1]:
                            if c + next_char == ">=" or c + next_char == ">=" or \
                            c + next_char == "==" or c + next_char == "!=" or \
                            c + next_char == "&&" or c + next_char == "||" or \
                            c + next_char == "->" and next_char != None:
                                tokens.append(Token(type="COMPARES", token=token, value=v))
                                i += len(v);
                                break
                            else:
                                continue
                        else:
                            if c == '>' or c == '<' or c == '!'\
                            and next_char != None:
                                tokens.append(Token(type="COMPARES", token=token, value=v))
                                i += len(v)
                                break
                if tokens != pre_addition_tok_list:
                    continue
                for token, v in TYPE.items():
                    if not next_char_eof:
                        if content[i:i + 3] == TYPE[token] and content[i + 3] not in ALPHANUMERIC:
                            tokens.append(Token(type="TYPE", token=token, value=content[i:i + 3]))
                            i += len(content[i:i + 3])
                            break
                        elif content[i:i + 4] == TYPE[token] and content[i + 4] not in ALPHANUMERIC:
                            tokens.append(Token(type="TYPE", token=token, value=content[i:i + 4]))
                            i += len(content[i:i + 4])
                            break
                        elif content[i:i + 5] == TYPE[token] and content[i + 5] not in ALPHANUMERIC:
                            tokens.append(Token(type="TYPE", token=token, value=content[i:i + 5]))
                            i += len(content[i:i + 5])
                            break
                        elif content[i:i + 6] == TYPE[token] and content[i + 6] not in ALPHANUMERIC:
                            tokens.append(Token(type="TYPE", token=token, value=content[i:i + 6]))
                            i += len(content[i:i + 6])
                            break
                    else: break
                if tokens != pre_addition_tok_list:
                    continue
                for token, v in KEYWORDS.items():
                    if not next_char_eof:
                        if content[i:i + 2] == KEYWORDS[token] and content[i + 2] not in ALPHANUMERIC:
                            tokens.append(Token(type="KEYWORD", token=token, value=content[i:i + 2]))
                            i += len(content[i:i + 2])
                            break
                        elif content[i:i + 3] == KEYWORDS[token] and content[i + 3] not in ALPHANUMERIC:
                            tokens.append(Token(type="KEYWORD", token=token, value=content[i:i + 3]))
                            i += len(content[i:i + 3])
                            break
                        elif content[i:i + 4] == KEYWORDS[token] and content[i + 4] not in ALPHANUMERIC:
                            tokens.append(Token(type="KEYWORD", token=token, value=content[i:i + 4]))
                            i += len(content[i:i + 4])
                            break
                        elif content[i:i + 5] == KEYWORDS[token] and content[i + 5] not in ALPHANUMERIC:
                            tokens.append(Token(type="KEYWORD", token=token, value=content[i:i + 5]))
                            i += len(content[i:i + 5])
                            break
                        elif content[i:i + 6] == KEYWORDS[token] and content[i + 6] not in ALPHANUMERIC:
                            tokens.append(Token(type="KEYWORD", token=token, value=content[i:i + 6]))
                            i += len(content[i:i + 6])
                            break
                        elif content[i:i + 8] == KEYWORDS[token] and content[i + 8] not in ALPHANUMERIC:
                            tokens.append(Token(type="KEYWORD", token=token, value=content[i:i + 8]))
                            i += len(content[i:i + 8])
                            break
                if tokens != pre_addition_tok_list:
                    continue
                for number in NUMBERS_WDOT:
                    dot_seen = False
                    too_many_dots = False
                    if c == number and not next_char_eof and (number != '.' or content[i + 1] in NUMBERS):
                        j = i
                        num = content[j]; j += 1

                        if content[j - 1] == "." and content[j] in NUMBERS:
                            too_many_dots = True
                            dot_seen = True

                        while not j + 1 >= len(content) and content[j] in NUMBERS_WDOT:
                            if content[j] == "." and not dot_seen:
                                dot_seen = True
                            elif content[j] == "." and dot_seen:
                                too_many_dots = True
                            num += content[j]
                            j += 1

                        if not too_many_dots: 
                            i += len(num)
                            if num[len(num) - 1] == ".": 
                                num += "0"
                            tokens.append(Token(type="NUMBER", token="TOKEN_NUMBER", value=num))
                        else: 
                            i += len(num)
                            if num[len(num) - 1] == ".": 
                                num += "0"
                            tokens.append(Token(type="NUMBER", token="TOKEN_MALFORMEDNUM", value=num)); 
                        break
                    else: continue
                if tokens != pre_addition_tok_list:
                    continue
                for token, v in PUNCTUATION.items():
                    if c == v:
                        tokens.append(Token(type="PUNCTUATION", token=token, value=v))
                        i += 1
                        break
                    else: continue
                if tokens != pre_addition_tok_list:
                    continue
                if c == ";":
                    tokens.append(Token(type="MISC", token="TOKEN_SEMI", value=c))
                    i += 1
                    continue

                if c == ' ':
                    tokens.append(Token(type="MISC", token="TOKEN_SPACE", value=' '))
                    i += 1
                    continue

                if c == "#":
                    j = i + 1
                    comment = c
                    if not next_char_eof:
                        while not j + 1 > len(content) and content[j] != "\n":
                            comment += content[j]
                            j += 1

                    tokens.append(Token(type="COMMENT", token="TOKEN_COMMENT", value=comment))
                    if not next_char_eof: i += len(comment); continue
                    else: break

                if c == '"':
                    j = i + 1
                    string = c
                    if not next_char_eof:
                        while not j + 1 > len(content) and content[j] != '"':
                            string += content[j]
                            j += 1
                        if not j + 1 > len(content): string += '"'

                    if string[len(string) - 1] == '"':
                        tokens.append(Token(type="STRING", token="TOKEN_STRING", value=string))
                        if not next_char_eof: i += len(string); continue
                        else: break
                    else:
                        tokens.append(Token(type="UNTERM_STRING", token="TOKEN_UNTERMSTR", value=string))
                        if not next_char_eof: i += len(string); continue
                        else: break

                if c == "'":
                    j = i + 1
                    char = c
                    if not next_char_eof:
                        char += content[j]
                        if not j + 1 >= len(content): 
                            if content[j + 1] == "'": char += "'"; char_unterm = False
                            else: char_unterm = True
                        else: char_unterm = True
                    else:
                        char_unterm = True

                    if char[len(char) - 1] == "'" and not char_unterm:
                        tokens.append(Token(type="CHAR", token="TOKEN_CHAR", value=char))
                        if not next_char_eof: i += len(char); continue
                        else: break
                    else:
                        tokens.append(Token(type="CHARTOOLONG", token="TOKEN_CHARTOOLONGORUNTERM", value=char))
                        if not next_char_eof: i += len(char); continue
                        else: break
                
                j = i
                identifier = ""
                if not next_char_eof:
                    while content[j] not in OPERATORS.values() and \
                    content[j] not in COMPARES.values() and \
                    content[j] not in TYPE.values() and \
                    content[j] not in PUNCTUATION.values() and \
                    content[j] not in DISALLOW:
                        identifier += content[j]
                        j += 1
                else:
                    identifier = content[i]

                tokens.append(Token(type="IDENTIFIER", token="TOKEN_VARID", value=identifier))
                if not next_char_eof: i += len(identifier); continue
                else: break
        return tokens