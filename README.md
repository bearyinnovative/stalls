Stalls
======

[https://en.wikipedia.org/wiki/Places_in_Harry_Potter#Stalls](https://en.wikipedia.org/wiki/Places_in_Harry_Potter#Stalls)

## Development

#### 1. Install pip

[Installing with get-pip.py](https://bootstrap.pypa.io/get-pip.py)

#### 2. Install virtualenv

`$ pip install virtualenv`

#### 3. Install pip-tools

`$ sudo pip install --upgrade pip`

`$ sudo pip install pip-tools`

#### 4. Create virtual environment

`$ virtualenv venv`

#### 5. Activate virtual environment

`$ . ./venv/bin/activate`

#### 6. Install dependencies

`$ pip install -r requirements.txt`

#### 7. Environment configuartion

`$ cp .env.sample .env`

Edit `.env` according to your envrionments.

#### 8. Start server

`$ honcho start`

## Update translations

```sh
$ ./babel.sh pot
$ ./babel.sh update

(edit translations files)

$ ./babel.sh build
```
