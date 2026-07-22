from .models import Sponsor


def sponsors_processor(request):

    sponsors = Sponsor.objects.filter(
        active=True
    )

    return {
        'footer_sponsors': sponsors
    }




from django.utils import timezone
from .models import Advertisement

def advertisements(request):
    now = timezone.now()

    return {
        "top_ads": Advertisement.objects.filter(
            active=True,
            position="top",
            start_date__lte=now,
            end_date__gte=now
        ),

        "sidebar_ads": Advertisement.objects.filter(
            active=True,
            position="sidebar",
            start_date__lte=now,
            end_date__gte=now
        ),

        "bottom_ads": Advertisement.objects.filter(
            active=True,
            position="bottom",
            start_date__lte=now,
            end_date__gte=now
        ),
    }