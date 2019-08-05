import rpy2.robjects as robjects
from bs4 import BeautifulSoup as BS4
from rpy2.robjects.packages import importr
import json
from email_reply_parser import EmailReplyParser

'''
NLoN training
'''
def training_nlon():
    nlon = importr('NLoN')
    #Path to NLoN training data
    robjects.r['load']('data/training_data.rda')

    return nlon, nlon.NLoNModel(robjects.r['text'], robjects.r['rater'])
'''
Gets mail corpus from email addresses
'''
def get_mail_corpus(nlon_cleaning=False):
    if (nlon_cleaning):
        nlon, nlon_model = training_nlon()

    #Path to mail's corpus
    corpus_file = 'data/mailcorpus.json'
    with open(corpus_file) as data_file:
        corpus = json.load(data_file)

    print('Reading and cleaning emails corpus. Number of emails: ' + str(len(corpus)))
    dict = {}
    n = 0
    #Text cleaning
    for d in corpus:
        if d['type_of_recipient'] == 'From':
            # if not d['is_response_of'] == None:
            res = EmailReplyParser.read(d['message_body'].replace('\\n', '\n'))
            text = res.reply
            # else:
            #     text = d['message_body'].replace('\\n', '\n')
            n += 1

            if (nlon_cleaning):
                try:
                    soup = BS4(text, 'html.parser')
                    clean_message_body = soup.text
                except Exception as e:
                    print('Error with BS4 on text:\n\n%s\n\n' % text, str(e))
                    clean_message_body = text.strip()
                message_by_lines = text.splitlines()
                list_length = len(message_by_lines)
                index = 0
                for count in range(0, list_length):
                    text1 = robjects.StrVector([message_by_lines[index]])
                    if nlon.NLoNPredict(nlon_model, text1)[0] == 'Not':
                        del message_by_lines[index]
                    else:
                        index = index + 1
                clean_message_body = '\n'.join(message_by_lines)
                text = clean_message_body

            if not text == '':
                if d['email_address'] in dict:
                    dict[d['email_address']].append(text)
                else:
                    dict[d['email_address']] = [text]
        print(str(n)+'/'+str(len(corpus))+'\n' if n%50==0 else '', end='')

    print('Mails retrieved: '+ str(n))
    print('Email addresses: '+ str(len(dict)))
    return dict