from django.contrib import admin
from .models import Tag, Topic, Roadmap, Unit, Item #,Membership

# Register your models here.
admin.site.register(Topic)
# admin.site.register(Membership)
admin.site.register(Roadmap)
admin.site.register(Unit)
admin.site.register(Item)
admin.site.register(Tag)