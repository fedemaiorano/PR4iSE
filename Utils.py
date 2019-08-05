import json as js
import statistics
import pandas as pd
import os

with open('data/mailingList', 'r') as ml_file:
    ml = [line.strip() for line in ml_file]

with open('data/results-11-04-19.json') as result_file:
    result = js.load(result_file)

def get_mails():
    mails = []
    for p in result:
        time = sum(x * int(t) for x, t in zip([60, 1], p['time'].split(":")))
        if (time > 100 and not p['email'].strip()=='Anonymous User' and not p['email'].strip() in ml):
            mails.append(p['email'].strip())

    with open('data/lista_mail.txt', 'w') as f:
        for item in mails:
            f.write(item + ', ')

    return mails

def get_binary_scores(mails, task_num, output_file):
    openness = []
    conscientiousness = []
    extraversion = []
    agreeableness = []
    neuroticism = []

    for p in result:
        openness.append(p['openness'])
        conscientiousness.append(p['coscientiousness'])
        extraversion.append(p['extraversion'])
        agreeableness.append(p['agreeableness'])
        neuroticism.append(p['neuroticism'])

    facts = {'1': 1, '2': 0.5, '3': 0}
    fact = facts[task_num]

    meanOPE = statistics.mean(openness)
    sdOPE = fact * statistics.stdev(openness)
    meanCON = statistics.mean(conscientiousness)
    sdCON = fact * statistics.stdev(conscientiousness)
    meanEXT = statistics.mean(extraversion)
    sdEXT = fact * statistics.stdev(extraversion)
    meanAGR = statistics.mean(agreeableness)
    sdAGR = fact * statistics.stdev(agreeableness)
    meanNEU = statistics.mean(neuroticism)
    sdNEU = fact * statistics.stdev(neuroticism)

    rows = {}
    for p in result:
        time = sum(x * int(t) for x, t in zip([60, 1], p['time'].split(":")))
        if (time > 100 and not p['email'].strip() == 'Anonymous User' and not p['email'].strip() in ml):
            row = []
            if (p['openness']) > meanOPE + sdOPE:
                row.append('H')
            elif (p['openness']) < meanOPE - sdOPE:
                row.append('L')
            else:
                row.append('n')

            if (p['coscientiousness']) > meanCON + sdCON:
                row.append('H')
            elif (p['coscientiousness']) < meanCON - sdCON:
                row.append('L')
            else:
                row.append('n')

            if (p['extraversion']) > meanEXT + sdEXT:
                row.append('H')
            elif (p['extraversion']) < meanEXT - sdEXT:
                row.append('L')
            else:
                row.append('n')

            if (p['agreeableness']) > meanAGR + sdAGR:
                row.append('H')
            elif (p['agreeableness']) < meanAGR - sdAGR:
                row.append('L')
            else:
                row.append('n')

            if (p['neuroticism']) > meanNEU + sdNEU:
                row.append('H')
            elif (p['neuroticism']) < meanNEU - sdNEU:
                row.append('L')
            else:
                row.append('n')

            rows[p['email'].strip()] = row

    df = pd.DataFrame(columns=['ID', 'cOPE', 'cCON', 'cEXT', 'cAGR', 'cNEU'])
    id = 0
    for k in mails:
        df.loc[id] = [k, rows[k][0], rows[k][1], rows[k][2], rows[k][3], rows[k][4]]
        id += 1

    df.to_csv(output_file, sep=',', encoding='utf-8', index=False, header=True)

    return df

def get_feature_csv_from_arff(input_arff, output_csv, score_csv):

    #Read and clean arff file
    _encoding = 'utf-8'
    arff_path = input_arff
    csv_path = arff_path + 'csv'
    with open(arff_path, 'r', encoding=_encoding) as fr:
        attributes = []
        write_sw = False
        with open(csv_path, 'w', encoding=_encoding) as fw:
            for line in fr.readlines():
                if write_sw:
                    fw.write(line)
                elif '@data' in line:
                    fw.write(','.join(attributes) + '\n')
                    write_sw = True
                elif '@attribute' in line:
                    attributes.append(line.split()[1])

    #Read result as csv
    import pandas as pd
    import re

    df = pd.read_csv(csv_path)
    os.remove(csv_path)
    for i in range(0,len(df)):
        df.iloc[i, df.columns.get_loc('filename')] = re.search('(.*\/)(.*)(\.txt)', df['filename'][i]).groups()[1]

    #Remove useless columns
    df.drop([list(df)[len(df.columns) - i] for i in range(1, 6)], axis=1, inplace=True)
    df.drop(['BROWN-FREQ','K-F-FREQ','K-F-NCATS','K-F-NSAMP','T-L-FREQ'], axis=1, inplace=True)

    #Replace '?' with 0
    for i in range(0,len(df)):
        df.iloc[i] = df.iloc[i].replace('?','0')

    #Merge result csv and mails_score csv
    df1 = pd.read_csv(score_csv, sep=',')

    df2 = pd.merge(left=df,right=df1, left_on='filename', right_on='ID')
    df2.drop(['filename'], axis=1, inplace=True)
    df2.to_csv(output_csv,index=False)

def get_multiclass_scores(mails, output_file, task_7 = False):
    openness = []
    conscientiousness = []
    extraversion = []
    agreeableness = []
    neuroticism = []

    for p in result:
        openness.append(p['openness'])
        conscientiousness.append(p['coscientiousness'])
        extraversion.append(p['extraversion'])
        agreeableness.append(p['agreeableness'])
        neuroticism.append(p['neuroticism'])

    fact = 1

    meanOPE = statistics.mean(openness)
    sdOPE = fact * statistics.stdev(openness)
    meanCON = statistics.mean(conscientiousness)
    sdCON = fact * statistics.stdev(conscientiousness)
    meanEXT = statistics.mean(extraversion)
    sdEXT = fact * statistics.stdev(extraversion)
    meanAGR = statistics.mean(agreeableness)
    sdAGR = fact * statistics.stdev(agreeableness)
    meanNEU = statistics.mean(neuroticism)
    sdNEU = fact * statistics.stdev(neuroticism)

    rows = {}
    for p in result:
        time = sum(x * int(t) for x, t in zip([60, 1], p['time'].split(":")))
        if (time > 100 and not p['email'].strip() == 'Anonymous User' and not p['email'].strip() in ml):
            row = []
            if (p['openness']) > meanOPE + sdOPE:
                row.append('H')
            elif (p['openness']) < meanOPE - sdOPE:
                row.append('L')
            elif (p['openness']) > meanOPE - 0.5 * statistics.stdev(openness) and (p['openness']) < meanOPE + 0.5 * statistics.stdev(openness):
                row.append('M')
            elif task_7 and (p['openness']) < meanOPE - 0.5 * statistics.stdev(openness):
                row.append('ll')
            elif task_7 and (p['openness']) > meanOPE + 0.5 * statistics.stdev(openness):
                row.append('hh')
            else:
                row.append('n')

            if (p['coscientiousness']) > meanCON + sdCON:
                row.append('H')
            elif (p['coscientiousness']) < meanCON - sdCON:
                row.append('L')
            elif (p['coscientiousness']) > meanCON - 0.5 * statistics.stdev(conscientiousness) and (p['coscientiousness']) < meanCON + 0.5 * statistics.stdev(conscientiousness):
                row.append('M')
            elif task_7 and (p['coscientiousness']) < meanCON - 0.5 * statistics.stdev(conscientiousness):
                row.append('ll')
            elif task_7 and (p['coscientiousness']) > meanCON + 0.5 * statistics.stdev(conscientiousness):
                row.append('hh')
            else:
                row.append('n')

            if (p['extraversion']) > meanEXT + sdEXT:
                row.append('H')
            elif (p['extraversion']) < meanEXT - sdEXT:
                row.append('L')
            elif (p['extraversion']) > meanEXT - 0.5 * statistics.stdev(extraversion) and (p['extraversion']) < meanEXT + 0.5 * statistics.stdev(extraversion):
                row.append('M')
            elif task_7 and (p['extraversion']) < meanEXT - 0.5 * statistics.stdev(extraversion):
                row.append('ll')
            elif task_7 and (p['extraversion']) > meanEXT + 0.5 * statistics.stdev(extraversion):
                row.append('hh')
            else:
                row.append('n')

            if (p['agreeableness']) > meanAGR + sdAGR:
                row.append('H')
            elif (p['agreeableness']) < meanAGR - sdAGR:
                row.append('L')
            elif (p['agreeableness']) > meanAGR - 0.5 * statistics.stdev(agreeableness) and (p['agreeableness']) < meanAGR + 0.5 * statistics.stdev(agreeableness):
                row.append('M')
            elif task_7 and (p['agreeableness']) < meanAGR - 0.5 * statistics.stdev(agreeableness):
                row.append('ll')
            elif task_7 and (p['agreeableness']) > meanAGR + 0.5 * statistics.stdev(agreeableness):
                row.append('hh')
            else:
                row.append('n')

            if (p['neuroticism']) > meanNEU + sdNEU:
                row.append('H')
            elif (p['neuroticism']) < meanNEU - sdNEU:
                row.append('L')
            elif (p['neuroticism']) > meanNEU - 0.5 * statistics.stdev(neuroticism) and (p['neuroticism']) < meanNEU + 0.5 * statistics.stdev(neuroticism):
                row.append('M')
            elif task_7 and (p['neuroticism']) < meanNEU - 0.5 * statistics.stdev(neuroticism):
                row.append('ll')
            elif task_7 and (p['neuroticism']) > meanNEU + 0.5 * statistics.stdev(neuroticism):
                row.append('hh')
            else:
                row.append('n')

            rows[p['email'].strip()] = row

    df = pd.DataFrame(columns=['ID', 'cOPE', 'cCON', 'cEXT', 'cAGR', 'cNEU'])
    id = 0
    for k in mails:
        df.loc[id] = [k, rows[k][0], rows[k][1], rows[k][2], rows[k][3], rows[k][4]]
        id += 1

    df.to_csv(output_file, sep=',', encoding='utf-8', index=False, header=True)

    return df

def get_continuous_scores(mails, output_file):
    rows = {}
    for p in result:
        time = sum(x * int(t) for x, t in zip([60, 1], p['time'].split(":")))
        if (time > 100 and not p['email'].strip() == 'Anonymous User' and not p['email'].strip() in ml):
            row = []
            row.append(p['openness'])
            row.append(p['coscientiousness'])
            row.append(p['extraversion'])
            row.append(p['agreeableness'])
            row.append(p['neuroticism'])

            rows[p['email'].strip()] = row

    df = pd.DataFrame(columns=['ID', 'cOPE', 'cCON', 'cEXT', 'cAGR', 'cNEU'])
    id = 0
    for k in mails:
        df.loc[id] = [k, rows[k][0], rows[k][1], rows[k][2], rows[k][3], rows[k][4]]
        id += 1

    df.to_csv(output_file, sep=',', encoding='utf-8', index=False, header=True)

    return df