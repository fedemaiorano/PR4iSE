import Utils as ut
import MailCorpus as mc
import Ngrams as ng
import sys, getopt
import pandas as pd

def main(argv):
    task_num = 0
    arff_file = ''
    nlon_cleaning = False
    try:
        opts, args = getopt.getopt(argv,"ht:i:nlon",["task_num=","ifile="])
    except getopt.GetoptError:
        print('feature_extraction.py -t <task_num> [-nlon] -i <arff_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt=='-help':
            print('feature_extraction.py -t <task_num> [-nlon] -i <arff_file>')
            sys.exit()
        elif opt in ("-nlon"):
            nlon_cleaning = True
        elif opt in ("-t", "--tasknum"):
            task_num = int(arg)
        elif opt in ("-i", "--ifile"):
            arff_file = arg

    dict = mc.get_mail_corpus(nlon_cleaning)
    # output_dir = 'texts'
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)
    #
    # for k in dict.keys():
    #     text = '\n'.join(dict[k])
    #     with open(output_dir + '/' + str(k) + '.txt', "w") as text_file:
    #         print(text, file=text_file)

    score_file = ['classes_task', '.csv']
    if task_num in range(1,4):
        ut.get_binary_scores(sorted(dict.keys()), str(task_num), str(task_num).join(score_file))
    elif task_num == 4:
        ut.get_multiclass_scores(sorted(dict.keys()), str(task_num).join(score_file))
    elif task_num == 7:
        ut.get_multiclass_scores(sorted(dict.keys()), str(task_num).join(score_file), task_7=True)
    elif task_num == 8:
        ut.get_continuous_scores(sorted(dict.keys()), str(task_num).join(score_file))
    else:
        print('Wrong task number')
        print('feature_extraction.py -t <task_num> [-nlon] -i <arff_file> -o <output_file>')
        sys.exit(2)

    ngram_df = ng.get_ngram_df(dict)

    feature_file = ['feature_task', '.csv']

    ut.get_feature_csv_from_arff(arff_file, str(task_num).join(feature_file), str(task_num).join(score_file))

    # Merge feature df with ngram_df
    feature_df = pd.read_csv(str(task_num).join(feature_file), sep=',')
    complete_df = pd.merge(left=ngram_df, right=feature_df, on='ID')
    complete_df.to_csv(feature_file[0] + str(task_num) + '_ngrams.csv', index=False)


if __name__ == "__main__":
   main(sys.argv[1:])