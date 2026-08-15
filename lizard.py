import tokenizer

tokens = tokenizer.tokenize("C:\\Users\\elias\\Documents\\Projects\\Lizard\\Source\\testing\\numbers_test.liz")

for t in tokens:
    print(t.type, t.token, repr(t.value))