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
```

#### Importing data
Within the same directory, create a 'data' folder containing files `gg2013.json` and `gg2015.json` with the appropriate data.

Twitter API integration will be added later.


#### Adding new packages
```
$ pip3 install <package-name>
$ pip3 show <package-name>
```
Add the package name with the version to requirements.txt

## Getting Started

This project runs on Python3, so any running of files or downloading of packages should be done with the appropriate commands ` $ python3 ` and ` $ pip `.
Once all the data and packages have been imported, then run:
```
$ python3 gg_api.py
```

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

## Authors
Group 1: Alex Rhee, Itay Golan, Arno Murica, Anthony Leonardi

See also the list of [contributors](https://github.com/alexr17/nlp-golden-globes/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
