from django.contrib import admin

from .models import Post

# Register your models here.

class PostModelAdmin(admin.ModelAdmin):

    list_display = ["__str__","timestamp"]
    class Meta:
        model = Post


admin.site.register(Post,PostModelAdmin)
