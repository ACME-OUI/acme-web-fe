acme-site
=========

###Overarching user interface for the acme project
**init**

    git clone git@github.com:aims-group/acme-site.git
    cd acme-site
    sudo pip install virtualenv
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt  
    python manage.py collectstatic

**setup**
    
    vim local_settings

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

###Changing HTML

    cd acme_site/templates/
    pwd  /path/acme-site/acme_site/templates
    vim base.html   <-- base layout will change all the pages
    vim home.html   <-- sites home page which extends base.html

    cd acme_site/
    pwd  /path/acme-site/acme_site/templates/acme_site
    vim *.html      <-- all pages content, they all include sidebars and extend base.html 
  
    cd acme_sidebars/
    pwd  /path/acme-site/acme_site/templates/acme_site/acme_sidebars
    vim *.html      <-- all sidebar partial pages, they are include in with content pages that extend base.html 

###Creating CSS

    <script> ... </script> put stlying in the file for now.

###Itergration
* https://github.com/globusonline/python-nexus-client 
