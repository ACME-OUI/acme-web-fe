acme-site
=========
[![Build Status](https://travis-ci.org/ACME-OUI/acme-web-fe.svg?branch=master)](https://travis-ci.org/ACME-OUI/acme-web-fe)
[![Coverage Status](https://coveralls.io/repos/github/sterlingbaldwin/acme-web-fe/badge.svg?branch=master)](https://coveralls.io/github/sterlingbaldwin/acme-web-fe?branch=master)
## Please Read the [Development Guidelines](https://github.com/ACME-OUI/acme-web-fe/wiki/Development-Guidelines)

###ACME Dashboard

####Python: This application requires  2.7.9 &lt; Python &lt; 3.0

**init**

    fork git@github.com:acme-oui/acme-web-fe.git
    git clone git@github.com:<your-user-name>/acme-web-fe.git
    cd acme-web-fe
    git remote add upstream http://github.com/acme-oui/acme-web-fe.git
    git fetch upstream

    sudo pip install virtualenv
    virtualenv env
    source env/bin/activate

    You need to have installed openssl, myproxy-devel, libffi

    pip install -U -r requirements.txt


    You will also need to install the django-sendfile module
    After creating your virtualenv and sourcing it,

    git clone https://github.com/johnsensible/django-sendfile
    cd django-sendfile
    python setup.py install

**local settings**

    cp local_settings.py.example local_settings.py
    vim local_settings.py

    Modify the settings for your local environment.

**static files**

   python manage.py collectstatic


**setup db**

    python manage.py syncdb

**setup admin**

    yes
    admin
    you@email.com
    password
    password

**update db**

    python manage.py migrate

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

**poller**

To get the job cycle working, download the llnl-poller from (here)[https://github.com/sterlingbaldwin/llnl-poller]
follow its install steps and run it before submitting jobs from the dashboard.
