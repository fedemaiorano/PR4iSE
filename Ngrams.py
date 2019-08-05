from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from collections import Counter

def get_ngram_df(dict_text):
    global dictG
    dictG = dict_text

    global ngram_set
    ngram_set = set()

    ngrams_dict = {}

    for k in dict_text.keys():
        s = '\n'.join(dict_text[k])
        s = s.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(s)
        # ngram_set |= set(ngrams(tokens, 1))
        # ngram_set |= set(ngrams(tokens, 2))
        count1 = Counter(ngrams(tokens, 1))
        count2 = Counter(ngrams(tokens, 1))
        for key, value in count1.items():
            if key in ngrams_dict:
                ngrams_dict[key] += value
            else:
                ngrams_dict[key] = value
        for key, value in count2.items():
            if key in ngrams_dict:
                ngrams_dict[key] += value
            else:
                ngrams_dict[key] = value

    ngrams_counts = Counter(ngrams_dict)
    ngram_set |= dict(ngrams_counts.most_common(10000)).keys()

    print('N-grams generation. Number of addresses:' + str(len(dict_text)))
    header = ['ID']
    header.extend(e for e in ('-'.join(w) for w in ngram_set))
    i = 0

    import concurrent.futures
    import time
    start_time = time.time()

    rows = []
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # Start the load operations and mark each future with its URL
        future_to_row = {executor.submit(get_ngrams_row, key): key for key in sorted(dict_text.keys())}
        for future in concurrent.futures.as_completed(future_to_row):
            id = future_to_row[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (id, exc))
            else:
                rows.append(data)
                i += 1
                print(str(i) + '/' + str(len(dict_text)) + '\n' if i % 5 == 0 else '', end='')

    print("--- %s seconds ---" % (time.time() - start_time))
    print('Number of n-grams: ' + str(len(ngram_set)))
    df = pd.DataFrame(columns=header, data=rows)
    return df


def get_ngrams_row(key):
    s = '\n'.join(dictG[key])
    s = s.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(s)

    ngram_row = {el: 0 for el in ngram_set}
    for n in ngrams(tokens, 1):
        if n in ngram_set:
            ngram_row[n] += 1
    for n in ngrams(tokens, 2):
        if n in ngram_set:
            ngram_row[n] += 1

    row = [key]
    row.extend(ngram_row[k] for k in ngram_set)
    return row







