from django.conf.urls import patterns, url

from warmup import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /users/form/add
    url(r'^form/add$', views.add_form, name='add_form'),
    # ex: /users/form/login
    url(r'^form/login$', views.login_form, name='login_form'),

    url(r'^form/reset$', views.reset_form, name='reset_form'),

    url(r'^form/test$', views.test_form, name='test_form'),

    # ex: /users/add
    url(r'^add$', views.add, name='add'),
    # ex: /users/login
    url(r'^login$', views.login, name='login'),

    url(r'^resetFixture$', views.reset, name='reset'),

    url(r'^unitTests$', views.run_test, name='run_test'),

)