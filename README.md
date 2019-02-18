# EECS 337 Project 1 Winter 2019

Explanation: 
This is the first project of EECS-337. The purpose of this project is to learn NLP techniques by scraping millions of tweets about the Golden Globes in order to determine information about the event, such as the host, who won Best Picture, etc.

### Installing
Clone this repo and install packages
```
$ git clone https://github.com/alexr17/nlp-golden-globes
$ cd nlp-golden-globes/
$ pip install -r requirements.txt
```
If you don't have pip you will need to install it.

Import nltk stopwords
```
$ python3
>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('punkt')
```

#### Importing data
Within the same directory, get the data: `gg2013.json` and `gg2015.json` from canvas and put it in the current, working directory. 


## Getting Started

This project runs on Python3, so any running of files or downloading of packages should be done with the appropriate commands ` $ python3 ` and ` $ pip `.
Once all the data and packages have been imported, then run:
```
$ python3 gg_api.py
```

This will print out the data in human, readable format including the presenters, nominees and winners for each award, along with the best, worst, and controversially dressed and best jokes. 

## Contributing

If you want to try solving different sections, rather than adding to the main branch, create your own branch:
```
$ git checkout -b <branch-name>
```
When you want to merge your changes
```
$ git checkout master
$ git merge <branch-name>
```
#### Adding new packages
```
$ pip3 install <package-name>
$ pip3 show <package-name>
```
If any packages have not been added, add the package name with the version to requirements.txt


## Authors
Group 1: Alex Rhee, Itay Golan, Arno Murica, Anthony Leonardi

See also the list of [contributors](https://github.com/alexr17/nlp-golden-globes/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
