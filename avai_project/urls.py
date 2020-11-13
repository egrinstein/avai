from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import avai_app.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", avai_app.views.index, name="index"),
    #path("db/", avai_app.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("detect/", avai_app.views.detect, name="detect"),
    #path("results/", avai_app.views.results, name="results"),
]
