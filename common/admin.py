from django.apps import apps
from django.contrib import admin

# add custom admin model here
custom_models = []

# this will register all the models in the admin pannell
models = apps.get_models()
for model in models:
    try:
        if model not in custom_models:
            admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
