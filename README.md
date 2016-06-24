acme-site
=========
[![Build Status](https://travis-ci.org/ACME-OUI/acme-web-fe.svg?branch=master)](https://travis-ci.org/ACME-OUI/acme-web-fe)
## Please Read the [Development Guidelines](https://github.com/ACME-OUI/acme-web-fe/wiki/Development-Guidelines)

###ACME Dashboard

####Python: This application requires  2.7.9 &lt; Python &lt; 3.0

**init**

    fork git@github.com:acme-oui/acme-web-fe.git
    git clone git@github.com:username/acme-web-fe.git
    cd acme-web-fe
    git remote add upstream http://github.com/acme-oui/acme-web-fe.git
    git fetch upstream

    sudo pip install virtualenv
    virtualenv env
    source env/bin/activate

    You need to have installed openssl, myproxy-devel, libffi

    pip install -U -r requirements.txt

    _Note_
    If the Jpype install fails because of missing Python.h, you're missing the python dev tools.
    Simply: sudo apt-get install python-dev

    Additionally, if you're using a 64bit version of python, make sure you're also using a 64bit version of java.
    If you get a wrong arch error on a mac, you might have both 32 and 64 bit versions of java installed. The simplest solution is to add the line
        export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.7.0_79.jdk/"
    to your .bashrc

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

**Selenium**
    Follow the directions [here](https://code.google.com/p/robotframework-seleniumlibrary/wiki/InstallationInstructions) to install the Selenium library to work with the robotframework.

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

**Velo Service**

In addition to running the django server, in order to get velo functionality you will also need to run the velo service.
This can be done by opening an additional shell, and typing:

    python apps/velo/velo_service.py
