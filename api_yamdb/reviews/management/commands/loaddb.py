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
            if file in ('title', 'comment'):
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
                        a[attr] = row[i]
                        attr_bak = attr
                        if attr in ('title_id', 'genre_id', 'review_id'):
                            attr = attr[:-3]
                        if attr in ('title', 'genre', 'review', 'category'):
                            attr = attr.capitalize()
                            #print(attr)
                            c = globals()[attr];
                            a[attr.lower()] = c.objects.get(pk=row[i])


                    #print(a)
                    t=cl(**a)
                    t.save()


        return "OK"


    def add_arguments(self, parser):
        parser.add_argument(
        '-p',
        '--path',
        action='store',
        default=str(settings.BASE_DIR)+'/static/data',
        help='Path to .csv files'
        )
