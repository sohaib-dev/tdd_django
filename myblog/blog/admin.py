from django.contrib import admin

from .models import Entry
from .models import Comment

admin.site.register(Entry)
admin.site.register(Comment)
