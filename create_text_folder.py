import MailCorpus as mc
import sys, getopt, os
import csv

def main(argv):
    input_dataset = ''
    output_dir = ''
    dataset_path = ''
    nlon_cleaning = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:p:nlon",["inputdataset=","outputdir=","datasetpath="])
    except getopt.GetoptError:
        print('create_text_folder.py -i Apache|LIWC [-nlon] [-p <dataset_path>] -o <output_dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt=='-help':
            print('create_text_folder.py -i Apache|LIWC [-nlon] [-p <dataset_path>] -o <output_dir>')
            sys.exit()
        elif opt in ("-nlon"):
            nlon_cleaning = True
        elif opt in ("-i", "--inputdataset"):
            input_dataset = arg
        elif opt in ("-o", "--outputdir"):
            output_dir = arg
        elif opt in ("-p", "--datasetpath"):
            dataset_path = arg

    print('Dataset: '+ str(input_dataset))
    print('NLoN: '+ str(nlon_cleaning))
    print('Dataset path: ' + dataset_path)
    print('Output directory: ' + output_dir)

    dict = {}
    if input_dataset == 'Apache':
        dict = mc.get_mail_corpus(nlon_cleaning)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for k in dict.keys():
            text = '\n'.join(dict[k])
            with open(output_dir + '/' + str(k) + '.txt', "w") as text_file:
                print(text, file=text_file)

    else:
        if dataset_path == '':
            print('Wrong input dataset')
            print('create_text_folder.py -i Apache|LIWC [-nlon] [-p <dataset_path>] -o <output_dir>')
            sys.exit()

        else:
            if input_dataset == 'LIWC':
                # Path to liwc gold standard
                # header is 'ID,text,cEXT,cNEU,cAGR,cCON,cOPN'

                with open(dataset_path, encoding='cp1252') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        dict[row[0]] = row[1]

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                for k in dict.keys():
                    with open(output_dir + '/' + str(k), "w") as text_file:
                        print(dict[k], file=text_file)

            else:
                print('Wrong input dataset')
                print('create_text_folder.py -i Apache|LIWC [-nlon] [-p <dataset_path>] -o <output_dir>')
                sys.exit()


if __name__ == "__main__":
   main(sys.argv[1:])