===============
Aineko newsbot
===============

Install on windows
-------------------
1. Install lxml for windows http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
2. pip install -r requirements.txt
3. curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3

Install on *nix/mac
-------------------
1. pip install -r requirements.txt
2. curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3


## TODO: 
1. Create healthcheck that checks connection to elasticsearch
2. implement rest service to store/fetch urls
3. Create healthcheck to verify connection to rest services as well