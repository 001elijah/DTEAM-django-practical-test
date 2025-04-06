from django.contrib import admin

from .models import BioItem, Contact, ContactType, Project, Skill, User

admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(BioItem)
admin.site.register(ContactType)
admin.site.register(Contact)
