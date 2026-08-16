from django.contrib import admin

from .models import (
    Province,
    Constituency,
    Party,
    Candidate,
    Result,
    Sponsor,
    NewsUpdate,
    Advertisement,
    Music,
)


admin.site.register(Province)
admin.site.register(Constituency)
admin.site.register(Party)
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'party',
        'total_votes',
    )

    list_editable = (
        'total_votes',
    )

    search_fields = (
        'name',
        'party__name',
    )
admin.site.register(Result)
admin.site.register(Sponsor)
admin.site.register(NewsUpdate)
admin.site.register(Advertisement)
admin.site.register(Music)