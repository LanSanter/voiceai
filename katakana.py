from janome.tokenizer import Tokenizer
import pandas as pd
import alkana
import re
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

alphaReg = re.compile(r'^[a-zA-Z]+$')
def isalpha(s):
    return alphaReg.match(s) is not None

def katakana_converter(text):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)

    df = pd.DataFrame([(t.surface, t.part_of_speech.split(',')[0]) for t in tokens], columns=["word", "part_of_speech"])
    df = df[df["part_of_speech"].str.startswith('名詞,固有名詞,人名') == True]
    df["english_word"] = df["word"].apply(isalpha)
    df = df[df["english_word"] == True]
    df["katakana"] = df["word"].apply(alkana.get_kana)

    dict_rep = dict(zip(df["word"], df["katakana"]))

    for word, read in dict_rep.items():
        try:
            text = text.replace(word, read)
        except:
            pass

    return text