from collections import Counter
import csv
import Utils as ut
import Ngrams as ng
import sys, getopt
import pandas as pd

def main(argv):
    arff_file = ''
    score_file = ''
    myPersonality_path = ''
    try:
        opts, args = getopt.getopt(argv, "hp:s:i:", ["mypersonalitydataset=", "scorefile=", "ifile="])
    except getopt.GetoptError:
        print('myPersonality_feature_extraction.py -p <myPersonality_dataset> -s <score_file> -i <arff_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '-help':
            print('myPersonality_feature_extraction.py -p <myPersonality_dataset> -s <score_file> -i <arff_file>')
            sys.exit()
        elif opt in ("-p", "--mypersonalitydataset"):
            myPersonality_path = arg
        elif opt in ("-s", "--scorefile"):
            score_file = arg
        elif opt in ("-i", "--ifile"):
            arff_file = arg

    if myPersonality_path == '' or arff_file == '' or score_file == '':
        print('myPersonality_feature_extraction.py -p <myPersonality_dataset> -s <score_file> -i <arff_file>')
        sys.exit()

    user_text = {}

    print('Reading myPersonality dataset (ca. 10 million status updates)')
    with open(myPersonality_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        n = 1
        next(csv_reader)
        for i in range(1, 9941273):
            row = next(csv_reader)
            key = row[2]
            if (key in user_text):
                user_text[key] = user_text[key] + '\n' + row[3]
            else:
                user_text[key] = row[3]
            #
            if (n % 1000000 == 0):
                print(n)
            n += 1
    csv_file.close()

    with open(score_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        temp_dict = {}
        for row in csv_reader:
            key = row[0]
            if key in user_text:
                temp_dict[key] = user_text[key]
        user_text = temp_dict

    c = Counter(user_text)
    mc = c.most_common(5000)
    user_text = dict(mc)

    for k in user_text.keys():
        s1 = user_text[k].split()[:100]
        str1 = ' '.join(s1)
        user_text[k] = [str1]

    ngram_df = ng.get_ngram_df(user_text)

    feature_file = ['feature_texts_', '.csv']

    df = pd.read_csv(score_file, delimiter=',')
    df.columns = map(str.upper, df.columns)
    df.to_csv(score_file, index=False)

    ut.get_feature_csv_from_arff(arff_file, 'myPersonality'.join(feature_file), score_file)

    # Merge feature df with ngram_df
    feature_df = pd.read_csv('myPersonality'.join(feature_file), sep=',')
    complete_df = pd.merge(left=ngram_df, right=feature_df, on='ID')
    complete_df.to_csv(feature_file[0] + 'myPersonality' + '_ngrams.csv', index=False)

if __name__ == "__main__":
   main(sys.argv[1:])


