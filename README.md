# Simple API for recommendations based on imported ALS taste vectors  
Logic is in hello/views.py

sim = np.dot(tovector,productFeaturesNumpy[:,1:].T)

e.g.
https://guarded-crag-2399.herokuapp.com/recov/7.3602986487918386e-24,%20-8.9922917229303507e-24,%202.6523794485599179e-23,%20-1.2612075438706492e-23,%201.2267009534962004e-23,%20-3.118138388676145e-23,%207.0755569384695972e-24,%207.2103290909611772e-24,%202.2941436697749432e-23,%20-1.9132319264972101e-23

https://guarded-crag-2399.herokuapp.com/reco/25

https://guarded-crag-2399.herokuapp.com/recot/65161040



based on: 

# python-getting-started

A barebones Python app, which can easily be deployed to Heroku.

This application support the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started
$ pip install -r requirements.txt
$ python manage.py syncdb
$ foreman start web
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master
$ heroku run python manage.py syncdb
$ heroku open
```

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

