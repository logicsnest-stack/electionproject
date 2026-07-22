from django.db import models
from ckeditor.fields import RichTextField


class Province(models.Model):

    name = models.CharField(
        max_length=100,
        db_index=True
    )

    def __str__(self):
        return self.name


class Constituency(models.Model):

    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name='constituencies'
    )

    name = models.CharField(
        max_length=100,
        db_index=True
    )

    class Meta:

        indexes = [

            models.Index(fields=['province']),

            models.Index(fields=['name']),

        ]

    def __str__(self):
        return self.name


class Party(models.Model):

    name = models.CharField(
        max_length=100,
        db_index=True
    )

    abbreviation = models.CharField(
        max_length=20,
        db_index=True
    )

    logo = models.ImageField(
        upload_to='party_logos/',
        blank=True,
        null=True
    )

    class Meta:

        indexes = [

            models.Index(fields=['name']),

            models.Index(fields=['abbreviation']),

        ]

    def __str__(self):
        return self.abbreviation


class Candidate(models.Model):

    name = models.CharField(
        max_length=100,
        db_index=True
    )

    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name='candidates'
    )

    photo = models.ImageField(
        upload_to='candidate_photos/',
        blank=True,
        null=True
    )

    class Meta:

        indexes = [

            models.Index(fields=['name']),

            models.Index(fields=['party']),

        ]

    def __str__(self):
        return self.name


class Result(models.Model):

    constituency = models.ForeignKey(
        Constituency,
        on_delete=models.CASCADE,
        related_name='results',
        db_index=True
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='results',
        db_index=True
    )

    votes = models.PositiveBigIntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = ('constituency', 'candidate')

        indexes = [

            models.Index(fields=['constituency']),

            models.Index(fields=['candidate']),

            models.Index(fields=['votes']),

            models.Index(fields=['updated_at']),

        ]

    def __str__(self):
        return f"{self.constituency} - {self.candidate}"


class Sponsor(models.Model):

    name = models.CharField(
        max_length=100,
        db_index=True
    )

    logo = models.ImageField(
        upload_to='sponsors/'
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    active = models.BooleanField(
        default=True,
        db_index=True
    )

    class Meta:

        indexes = [

            models.Index(fields=['active']),

            models.Index(fields=['name']),

        ]

    def __str__(self):
        return self.name


class NewsUpdate(models.Model):

    title = models.CharField(
        max_length=255,
        db_index=True
    )

    content = RichTextField()

    image = models.ImageField(
        upload_to='news_images/',
        blank=True,
        null=True
    )

    breaking = models.BooleanField(
        default=False,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['-created_at']

        indexes = [

            models.Index(fields=['created_at']),

            models.Index(fields=['breaking']),

            models.Index(fields=['title']),

        ]

    def __str__(self):
        return self.title


class Comment(models.Model):

    news = models.ForeignKey(
        NewsUpdate,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    name = models.CharField(
        max_length=100,
        db_index=True
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['-created_at']

        indexes = [

            models.Index(fields=['created_at']),

            models.Index(fields=['news']),

        ]

    def __str__(self):
        return self.name


class Reaction(models.Model):

    REACTION_CHOICES = (

        ('like', 'Like'),

        ('love', 'Love'),

        ('wow', 'Wow'),

    )

    news = models.ForeignKey(
        NewsUpdate,
        on_delete=models.CASCADE,
        related_name='reactions'
    )

    reaction_type = models.CharField(
        max_length=20,
        choices=REACTION_CHOICES,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        indexes = [

            models.Index(fields=['reaction_type']),

            models.Index(fields=['created_at']),

            models.Index(fields=['news']),

        ]

    def __str__(self):
        return self.reaction_type



class Advertisement(models.Model):
    POSITION_CHOICES = [
        ("top", "Top Banner"),
        ("middle", "Middle Banner"),
        ("bottom", "Bottom Banner"),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="advertisements/")
    link = models.URLField(blank=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)

    active = models.BooleanField(default=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]