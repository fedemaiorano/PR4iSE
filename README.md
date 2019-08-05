# PR4iSE - Personality Recognition for Software Engineering

## Fair use

If you decide to use this tool, please give us credit by citing the following works:

F. Calefato, F. Lanubile, and B. Vasilescu (2019) “[A large-scale, in-depth analysis of developers’ personalities in the Apache ecosystem](https://arxiv.org/abs/1905.13062).” Information and Software Technology, Vol. 114, Oct., pp. 1-20, DOI: [10.1016/j.infsof.2019.05.012](https://doi.org/10.1016/j.infsof.2019.05.012).

```
@article{Calefato:2019,
  title = "A large-scale, in-depth analysis of developers’ personalities in the Apache ecosystem",
  journal = "Information and Software Technology",
  volume = "114",
  pages = "1 - 20",
  year = "2019",
  issn = "0950-5849",
  doi = "https://doi.org/10.1016/j.infsof.2019.05.012",
  url = "http://www.sciencedirect.com/science/article/pii/S0950584918301216",
  author = "Fabio Calefato and Filippo Lanubile and Bogdan Vasilescu",
}
```

F. Calefato, G. Iaffaldano, F. Lanubile, B. Vasilescu (2018). “[On Developers’ Personality in Large-scale Distributed Projects: The Case of the Apache Ecosystem](https://arxiv.org/pdf/1803.01126).” In Proc. Int’l Conf. on Global Software Engineering (ICGSE’18), Gothenburg, Sweden, May 28-29, 2018, [DOI:10.1145/3196369.3196372](https://doi.org/10.1145/3196369.3196372).

```
@inproceedings{Calefato:2018,
  author = {Calefato, Fabio and Iaffaldano, Giuseppe and Lanubile, Filippo and Vasilescu, Bogdan},
  title = {On Developers' Personality in Large-scale Distributed Projects: The Case of the Apache Ecosystem},
  booktitle = {Proceedings of the 13th International Conference on Global Software Engineering},
  series = {ICGSE '18},
  year = {2018},
  isbn = {978-1-4503-5717-3},
  location = {Gothenburg, Sweden},
  pages = {92--101},
  numpages = {10},
  url = {http://doi.acm.org/10.1145/3196369.3196372},
  doi = {10.1145/3196369.3196372},
  acmid = {3196372},
  publisher = {ACM},
  address = {New York, NY, USA},
}
```

## Requirements

#### Python:
* Python 3.5.x
* NLTK 3.4
* pandas

#### R:
* liblineaR
* Rweka

## Installation
```
$ git clone https://github.com/collab-uniba/Personality-Recognition-in-SD.git
$ git submodule init
$ git submodule update
```

## Setup

1. Add the following file to the `data` folder:
  * `mailcorpus.json` containing Apache developers emails
  * `training_data.rda` model for [NLoN](https://github.com/M3SOulu/NLoN)
  * the json file containing the results of mini-IPIP test

2. Install packages via `pip`
```
$ pip install -r requirements.txt
```

## Pipeline (Apache)

1. Create a folder containing a text file for each Apache's developer, via the ```create_text_folder.py``` script:
```
$ python create_text_folder.py -i Apache -o output_dir
```
if you want the NLoN filtering add the ```-nlon``` parameter:
```
$ python create_text_folder.py -i Apache -nlon -o output_dir
```

2. Extract Mairesse's features using [PersonalityRecognizer](http://farm2.user.srcf.net/research/personality/recognizer), giving as input the folder created:
```
$ PersonalityRecognizer -i output_dir -d -t 2 -a mairesse_Apache.arff
```

3. Create 2 csv file with features (the first only with Mairesse's features, and the second also includes n-grams) using ```feature_extraction.py``` script, specifying the task number (between 1 and 8) and the ```-nlon``` flag if you want the NLoN filtering:
```
$ python feature_extraction.py -t task_num [-nlon] -i mairesse_Apache.arff
```
this script will also create a csv with class distributions

## Pipeline (LIWC)

1. Create a folder containing a text file for each LIWC's developer, via the ```create_text_folder.py``` script, giving as input the path to LIWC dataset (header structured as follows ```'ID,text,cEXT,cNEU,cAGR,cCON,cOPN'```):
```
$ python create_text_folder.py -i LIWC -p path_to_LIWC_dataset -o output_dir
```

2. Extract Mairesse's features using [PersonalityRecognizer](http://farm2.user.srcf.net/research/personality/recognizer), giving as input the folder created:
```
$ PersonalityRecognizer -i output_dir -d -t 2 -a mairesse_LIWC.arff
```

3. Create 2 csv file with features (the first only with Mairesse's features, and the second also includes n-grams) using ```LIWC_feature_extraction.py``` script:
```
$ python LIWC_feature_extraction.py -p path_to_LIWC_dataset -i mairesse_LIWC.arff
```
this script will also create a csv with class distributions

## Pipeline (myPersonality)

1. Create a folder containing a text file for each of the top 5000 myPersonality's user, via the ```create_text_folder_myPersonality.py``` script, giving as input the path to myPersonality dataset. ```path_to_myPersonality_dataset``` is the path of ```status_updates.csv``` (header is ```'"","messageid","userid","message","updated_time","nchar"'```). ```score_myPersonality``` is generated from ```big5.csv``` from myPersonality database (header structured as follows ```'"ID","ope","con","ext","agr","neu"'```):
```
$ python create_text_folder_myPersonality.py -p path_to_myPersonality_dataset -s score_myPersonality -o output_dir
```

2. Extract Mairesse's features using [PersonalityRecognizer](http://farm2.user.srcf.net/research/personality/recognizer), giving as input the folder created:
```
$ PersonalityRecognizer -i output_dir -d -t 2 -a mairesse_myPersonality.arff
```

3. Create 2 csv file with features (the first only with Mairesse's features, and the second also includes n-grams) using ```myPersonality_feature_extraction.py``` script:
```
$ python myPersonality_feature_extraction.py -p path_to_myPersonality_dataset -s score_myPersonality -i mairesse_myPersonality.arff
```
this script will also create a csv with class distributions

## Classification

Classification folder contains all the R script created for classification
