import csv
from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment 

class Command(BaseCommand):
    help = 'Load data from .csv to DB'

    def handle(self, *args, **options):
        print(f'Use path: {options["path"]}')

        for cl in (Category, Genre, Title, GenreTitle, Review, Comment):
            file = cl.__name__.lower()
            if file in ('title', 'comment', 'user'):
                file += 's'
            if file == 'genretitle':
                file = 'genre_title'

            print(f'Load file {file}.csv')
            with open(f'{options["path"]}/{file}.csv') as f:
                reader = csv.reader(f)
                attrs = None
                for row in reader:
                    if not attrs:
                        attrs = row
                        continue


                    a = dict()
                    for i, attr in enumerate(attrs):
                        if attr == 'author':
                            continue;
                        if attr in ('category',):
                            attr += '_id'
                        a[attr] = row[i]

                    (cl(**a)).save()

        return "OK"


    def add_arguments(self, parser):
        parser.add_argument(
        '-p',
        '--path',
        action='store',
        default=str(settings.BASE_DIR)+'/static/data',
        help='Path to .csv files'
        )
