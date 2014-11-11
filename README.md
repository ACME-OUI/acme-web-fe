acme-site
=========

###Overarching user interface for the acme project

    git clone git@github.com:aims-group/acme-site.git
    cd acme-site
    sudo pip install virtualenv
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt  
    python manage.py collectstatic
    python manage.py runserver 

If you have turned on websharing on your mac you can display it using
your machines url, eg 

    python manage.py runserver harris112ml.llnl.gov:8000

then from your browser you can view the site at 

* users front end
  * *yourMachineName*.llnl.gov:8000/acme
  * 127.0.0.1:8000/acme
* admin front end (**not implemented yet**)
  * *yourMachineName*.llnl.gov:8000/admin
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

###AKUNA api
* see the [wiki](https://github.com/aims-group/acme-site/wiki/AKUNA-API)
