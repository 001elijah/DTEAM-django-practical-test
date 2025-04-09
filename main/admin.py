from django.contrib import admin

from .models import (
    BioItem,
    Candidate,
    CandidateProject,
    CandidateSkill,
    Contact,
    ContactType,
    Project,
    Skill,
)

admin.site.register(Candidate)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(BioItem)
admin.site.register(ContactType)
admin.site.register(Contact)
admin.site.register(CandidateSkill)
admin.site.register(CandidateProject)
