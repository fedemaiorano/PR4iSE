from collections import Counter
import csv, os
import sys, getopt


def main(argv):
    score_file = ''
    myPersonality_path = ''
    output_dir = ''
    try:
        opts, args = getopt.getopt(argv, "hp:s:o:", ["mypersonalitydataset=", "scorefile=", "outputdir="])
    except getopt.GetoptError:
        print('create_text_folder_myPersonality.py -p <myPersonality_dataset> -s <score_file> -o <output_dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '-help':
            print('create_text_folder_myPersonality.py -p <myPersonality_dataset> -s <score_file> -o <output_dir>')
            sys.exit()
        elif opt in ("-p", "--mypersonalitydataset"):
            myPersonality_path = arg
        elif opt in ("-s", "--scorefile"):
            score_file = arg
        elif opt in ("-o", "--outputdir"):
            output_dir = arg

    if myPersonality_path == '' or score_file == '' or output_dir == '':
        print('create_text_folder_myPersonality.py -p <myPersonality_dataset> -s <score_file> -o <output_dir>')
        sys.exit()

    user_text = {}

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

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for k in user_text.keys():
        with open(output_dir + '/' + str(k) + '.txt', "w") as text_file:
            print(user_text[k], file=text_file)


if __name__ == "__main__":
    main(sys.argv[1:])


