acme-site
=========
[![Build Status](https://travis-ci.org/ACME-OUI/acme-web-fe.svg?branch=master)](https://travis-ci.org/ACME-OUI/acme-web-fe)
## Please Read the [Development Guidelines](https://github.com/ACME-OUI/acme-web-fe/wiki/Development-Guidelines)

###ACME Dashboard
**init**

    fork git@github.com:acme-oui/acme-web-fe.git
    git clone git@github.com:username/acme-web-fe.git
    cd acme-web-fe
    git remote add upstream http://github.com/acme-oui/acme-web-fe.git
    git fetch upstream

    sudo pip install virtualenv
    virtualenv env
    source env/bin/activate

    You need to have installed openssl or myproxy-devel

    pip install -r requirements.txt

**local settings**
    
    vim local_settings.py

**add this**

    import os.path

    STATICFILES_DIRS = (
        '/path/to/acme-web-fe/acme_site/static/',
    )

    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(os.path.abspath("."), 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
      }
    }

    #Get a key from the google registration page
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = ''

    JAR_PATH = '-Djava.class.path=/path/to/acme-web-fe/static/java/VeloAPI.jar'


**static files**

   python manage.py collectstatic

**Velo API**

    Open VeloAPI.py and change /Users/baldwin32/projects/acme-web-fe/acme_site/static/java/VeloAPI.jar to the location of your .jar file
    source env/bin/activate
    git clone https://github.com/originell/jpype.git
    cd jpype
    python setup.py install 
    cd ..
    rm -rf jpype
    
    _Note_
    If the Jpype install fails because of missing Python.h, you're missing the python dev tools. 
    Simply: sudo apt-get install python-dev

**setup db**

    python manage.py syncdb
    
**setup admin**

    yes
    admin
    you@email.com
    password
    password

**update db**

    python mange.py migrate

**running**

    python manage.py runserver 

If you have turned on websharing on your mac you can display it using your machines url, eg 

    python manage.py runserver boxname.domain:8000

then from your browser you can view the site at 

* users front end
  * *boxname.domain*:8000/acme
  * 127.0.0.1:8000/acme
* admin front end (**not implemented yet**)
  * *boxname.domain*:8000/admin
  * 127.0.0.1:8000/admin
