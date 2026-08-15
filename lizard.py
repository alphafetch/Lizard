import tokenizer

DEBUG = False
tokens = tokenizer.tokenize("C:\\Users\\elias\\Documents\\Projects\\Lizard\\Source\\testing\\test2.liz")

if DEBUG:
    for t in tokens:
        print(t.type, t.token, repr(t.value))