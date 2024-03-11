### Introduction

This repo will contains all my scripts that import transactions from investments brokers (crypto, bank, etc)

#### Bitstack
A mobile application where you can DCA your bitcoin.  
Please use my [Referral link](https://bitstack-app.com/referral/Jey_Jeg_%5B46%2C) if you're not registered on Bitstack-app and you would like to DCA some BTC (+5€ each).

### Installation for Python3

```
pipenv shell
pipenv install
```

```
cp settings.conf.example settings.conf
```

Modify values in file settings.conf and then launch your script on a previously downloaded transaction history csv.

```
python bitstack_app.py bitstack_2023.csv
```
