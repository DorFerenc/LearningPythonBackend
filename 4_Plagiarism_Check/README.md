# Plagiarism Check using spaCy

API to Check Similarity of 2 text documents with spaCy
Implements tokens to 'charge' for usage of API per registerd user

### Using spaCy Models
* https://spacy.io/models/en 
* https://spacy.io/usage/models 
* https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz


### API Chart Protocols

| Resource                  | Address   | Protocol | Parameters                                        | Responses + status code                                                                    |
| ------------------------- | --------- | -------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Register New User         | /register | POST     | username\|password\|{String}                      | 200 OK\| 301 Invalid Username                                                              |
| Detect similarity of docs | /detect   | POST     | username\|password\|text1\|text2\|{String}        | 200 OK return similarity\| 301 Invalid Username\| 302 Invalid passowrd\| 303 Out of tokens |
| Refill tokens             | /refill   | POST     | username\|adminPW\|refillAmount\|{String} | 200 OK\| 301 Invalid Username\| 304 Invalid admin passowrd                                 |