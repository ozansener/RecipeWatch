from django.contrib import admin
from recipe.models import RecipeQuery,Video,Text

admin.site.register(RecipeQuery)
admin.site.register(Text)
admin.site.register(Video)

# Register your models here.
