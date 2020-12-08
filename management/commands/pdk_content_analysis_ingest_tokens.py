# pylint: disable=no-member,line-too-long

from __future__ import print_function

import csv
import os

from django.core.management.base import BaseCommand

from passive_data_kit.decorators import handle_lock

from ...models import SentimentToken

class Command(BaseCommand):
    help = 'Ingests '

    def add_arguments(self, parser):
        parser.add_argument('tokens_csv',
                            help='Path to CSV file containing tokens, labels, and scores')

    @handle_lock
    def handle(self, *args, **options):
        basename = os.path.basename(options['tokens_csv']).split('.')[0]

        ingested = 0

        with open(options['tokens_csv'], 'rb') as csvfile:
            tokens_reader = csv.reader(csvfile)

            for row in tokens_reader:
                try:
                    token = row[0]
                    label = row[1]
                    score = float(row[2])

                    token = token.strip()

                    token = token.replace('\t', ' ')
                    token = token.replace('\n', ' ')
                    token = token.replace('\r', ' ')

                    while '  ' in token:
                        token = token.replace('  ', ' ')

                    size = len(token.split(' '))

                    if SentimentToken.objects.filter(source=basename, token=token, label=label, score=score, size=size).count() > 0:
                        print('Already found existing token: ' + basename + ' -- ' + str(token) + ' -- ' + str(label) + ' -- ' + str(score) + ' -- ' + str(size))
                    else:
                        SentimentToken(source=basename, token=token, label=label, score=score, size=size).save()

                        ingested += 1

                        if (ingested % 100) == 0:
                            print('Ingested ' + str(ingested) + ' new token(s).')
                except ValueError:
                    pass

        print('Ingested ' + str(ingested) + ' new token(s).')
