from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages

from django.db.models import Sum

  

from .models import (
    Constituency,
    Candidate,
    Result,
    NewsUpdate,
    Comment,
    Reaction,
)

from django.views.decorators.cache import cache_page

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Value




@cache_page(5)
def home(request):

    national_results = Candidate.objects.select_related(
        'party'
    ).annotate(
        total_votes=Coalesce(
            Sum('results__votes'),
            Value(0)
        )
    ).order_by(
        '-total_votes',
        'name'
    )

    total_votes = national_results.aggregate(
        total=Sum('total_votes')
    )['total'] or 0

    context = {
        'national_results': national_results,
        'total_votes': total_votes
    }

    return render(
        request,
        'results/home.html',
        context
    )


@cache_page(10)
def constituency_detail(request, constituency_id):

    constituency = get_object_or_404(
        Constituency.objects.select_related('province'),
        id=constituency_id
    )

    results = constituency.results.select_related(
        'candidate',
        'candidate__party'
    ).order_by('-votes')

    total_votes = results.aggregate(
        total=Sum('votes')
    )['total'] or 0

    context = {
        'constituency': constituency,
        'results': results,
        'total_votes': total_votes
    }

    return render(
        request,
        'results/constituency_detail.html',
        context
    )


@staff_member_required
def results_dashboard(request):

    query = request.GET.get("q", "")

    constituencies = Constituency.objects.select_related(
        "province"
    )

    if query:

        constituencies = constituencies.filter(
            name__icontains=query
        )

    candidates = Candidate.objects.select_related(
        'party'
    )

    if request.method == "POST":

        constituency_id = request.POST.get("constituency")

        candidate_id = request.POST.get("candidate")

        votes = request.POST.get("votes")

        if not (constituency_id and candidate_id and votes):

            messages.error(
                request,
                "All fields are required."
            )

            return redirect("results_dashboard")

        result, created = Result.objects.update_or_create(

            constituency_id=constituency_id,

            candidate_id=candidate_id,

            defaults={
                'votes': votes
            }
        )

        messages.success(
            request,
            "Result saved successfully!"
        )

        return redirect("results_dashboard")

    context = {
        "constituencies": constituencies,
        "candidates": candidates,
        "query": query
    }

    return render(
        request,
        "results/dashboard.html",
        context
    )

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.db.models import Value

from .models import (
    NewsUpdate,
    Comment,
    Reaction,
    Constituency
)


from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.db.models import Count

from .models import NewsUpdate


from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60)
def news_list(request):

    news_queryset = NewsUpdate.objects.annotate(
        comment_count=Count('comments', distinct=True),
        reaction_count=Count('reactions', distinct=True)
    ).order_by('-created_at')

    paginator = Paginator(news_queryset, 12)

    page_number = request.GET.get('page')

    news_updates = paginator.get_page(page_number)

    current_page = news_updates.number
    total_pages = paginator.num_pages

    start_page = max(current_page - 2, 1)
    end_page = min(current_page + 2, total_pages)

    page_range = range(start_page, end_page + 1)

    context = {
        'news_updates': news_updates,
        'page_range': page_range,
    }

    return render(
        request,
        'results/news_list.html',
        context
    )
def news_detail(request, news_id):

    news = get_object_or_404(
        NewsUpdate,
        id=news_id
    )

    if request.method == "POST":

        # COMMENTS

        if "content" in request.POST:

            name = request.POST.get("name")

            content = request.POST.get("content")

            if name and content:

                Comment.objects.create(
                    news=news,
                    name=name,
                    content=content
                )

        # REACTIONS

        if "reaction_type" in request.POST:

            reaction_type = request.POST.get(
                "reaction_type"
            )

            Reaction.objects.create(
                news=news,
                reaction_type=reaction_type
            )

        return redirect(
            'news_detail',
            news_id=news.id
        )

    comments = news.comments.order_by(
        '-created_at'
    )[:100]

    reactions = news.reactions.values(
        'reaction_type'
    ).annotate(
        total=Count('id')
    )

    reaction_counts = {
        'like': 0,
        'love': 0,
        'wow': 0
    }

    for reaction in reactions:

        reaction_counts[
            reaction['reaction_type']
        ] = reaction['total']

    context = {
        'news': news,
        'comments': comments,

        'like_count': reaction_counts['like'],
        'love_count': reaction_counts['love'],
        'wow_count': reaction_counts['wow'],
    }

    return render(
        request,
        'results/news_detail.html',
        context
    )


from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.cache import cache_page

@cache_page(30)
def constituencies(request):

    query = request.GET.get("q", "")

    constituencies = Constituency.objects.select_related(
        'province'
    ).prefetch_related(
        'results__candidate',
        'results__candidate__party'
    )

    if query:

        constituencies = constituencies.filter(
            name__icontains=query
        )

    paginator = Paginator(
        constituencies.order_by('-id'),
        20
    )

    page_number = request.GET.get('page')

    constituencies_page = paginator.get_page(
        page_number
    )

    constituency_data = []

    for constituency in constituencies_page:

        results = list(
            constituency.results.all().order_by(
                '-votes'
            )
        )

        if results:

            top_three = results[:3]

            others = results[3:]

            total_votes = sum(
                result.votes
                for result in results
            )

            constituency_data.append({
                'constituency': constituency,
                'top_three': top_three,
                'others': others,
                'total_votes': total_votes
            })

    context = {
        'constituency_data': constituency_data,
        'query': query,
        'constituencies_page': constituencies_page
    }

    return render(
        request,
        'results/constituencies.html',
        context
    )



def privacy_policy(request):
    return render(
        request,
        'results/privacy_policy.html'
    )


def terms_and_conditions(request):
    return render(
        request,
        'results/terms_and_conditions.html'
    )



def about(request):
    return render(
        request,
        'results/about.html'
    )

from django.shortcuts import render

def contact(request):
    return render(request, "results/contact.html")