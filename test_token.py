from preprocessing.tokenizer import preprocess_text

sample = "React hooks are causing infinite rerenders!"

tokens = preprocess_text(sample)

print(tokens)