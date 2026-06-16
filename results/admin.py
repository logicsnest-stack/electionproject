from django.contrib import admin

from .models import (
    Province,
    Constituency,
    Party,
    Candidate,
    Result,
    Sponsor,
    NewsUpdate
)


admin.site.register(Province)
admin.site.register(Constituency)
admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(Result)
admin.site.register(Sponsor)
admin.site.register(NewsUpdate)