import tokenizer
import parser

DEBUG_TOKENIZATION = False
DEBUG_PARSING = True
tokens = tokenizer.tokenize("C:\\Users\\elias\\Documents\\Projects\\Lizard\\Source\\testing\\test4.liz")

if DEBUG_TOKENIZATION:
    for t in tokens:
        print(t.type, t.token, repr(t.value))

tokens = parser.filter_token_list(tokens)

node, new_index = parser.parse_var_dec(tokens, 0)

if DEBUG_PARSING:
    print(node, node.type, node.name, node.val)
    print("new index: ", new_index)