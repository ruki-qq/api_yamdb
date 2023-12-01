import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    """Command to load data from csv files to DB."""

    FILENAMES_OF_MODELS = [
        ('users.csv', User),
        ('category.csv', Category),
        ('genre.csv', Genre),
        ('titles.csv', Title),
        ('genre_title.csv', Title.genre.through),
        ('review.csv', Review),
        ('comments.csv', Comment),
    ]

    help = 'Load data from .csv to DB'

    def handle(self, *args, **options):
        print(f'Use path: {options["path"]}')

        for filename, model in self.FILENAMES_OF_MODELS:
            print(f'Load file {filename}')
            with open(f'{options["path"]}/{filename}') as f:
                reader = csv.reader(f)
                attrs = None
                for row in reader:
                    if not attrs:
                        attrs = row
                        continue

                    data = {}
                    for i, attr in enumerate(attrs):
                        if attr in ('author', 'category'):
                            attr += '_id'
                        data[attr] = row[i]

                    model(**data).save()

        return 'OK'

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            action='store',
            default=str(settings.BASE_DIR) + '/static/data',
            help='Path to .csv files',
        )
