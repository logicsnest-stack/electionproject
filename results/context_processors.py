from .models import Sponsor


def sponsors_processor(request):

    sponsors = Sponsor.objects.filter(
        active=True
    )

    return {
        'footer_sponsors': sponsors
    }