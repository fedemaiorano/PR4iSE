import csv
import Utils as ut
import Ngrams as ng
import sys, getopt
import pandas as pd

def main(argv):
    arff_file = ''
    liwc_path = ''
    try:
        opts, args = getopt.getopt(argv,"hp:i:",["liwcdataset=","ifile="])
    except getopt.GetoptError:
        print('LIWC_feature_extraction.py -p <liwc_dataset> -i <arff_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt=='-help':
            print('LIWC_feature_extraction.py -p <liwc_dataset> -i <arff_file>')
            sys.exit()
        elif opt in ("-p", "--liwcdataset"):
            liwc_path = arg
        elif opt in ("-i", "--ifile"):
            arff_file = arg

    if liwc_path == '' or arff_file == '':
        print('LIWC_feature_extraction.py -p <liwc_dataset> -i <arff_file>')
        sys.exit()

    liwc_dict = {}

    with open(liwc_path, encoding='cp1252') as csv_file:
        df = pd.read_csv(csv_file, delimiter=',')

        text_column = df.columns[1]
        df = df.drop([text_column], axis=1)
        df.columns = ['ID', 'cEXT', 'cNEU', 'cAGR', 'cCON', 'cOPN']
        df.to_csv('score_liwc.csv', index=False)


    with open(liwc_path, encoding='cp1252') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            liwc_dict[row[0]] = row[1]

    for k in liwc_dict.keys():
        s1 = liwc_dict[k].split()[:100]
        str1 = ' '.join(s1)
        liwc_dict[k] = [str1]

    ngram_df_liwc = ng.get_ngram_df(liwc_dict)

    # arff generated with PersonalityRecognizer
    feature_file = ['feature_', '.csv']

    ut.get_feature_csv_from_arff(arff_file, 'liwc'.join(feature_file), 'score_liwc.csv')

    # Merge feature df with ngram_df
    feature_df = pd.read_csv('liwc'.join(feature_file), sep=',')
    complete_df = pd.merge(left=ngram_df_liwc, right=feature_df, on='ID')
    complete_df.to_csv(feature_file[0] + 'liwc' + '_ngrams.csv', index=False)

if __name__ == "__main__":
   main(sys.argv[1:])

