# pylint: disable=no-member,line-too-long

from __future__ import print_function

from django.core.management.base import BaseCommand

from passive_data_kit.decorators import handle_lock

from passive_data_kit.models import DataPoint

def process_item(item):
    word_count = 0
    character_count = 0

    if isinstance(item, dict):
        for key, value in item.iteritems():
            if key.startswith('pdk_length_'):
                character_count += value
            elif key.startswith('pdk_word_count_'):
                word_count += value
            elif isinstance(value, (list, dict,)):
                item_word_count, item_character_count = process_item(value)

                character_count += item_character_count
                word_count += item_word_count
    elif isinstance(item, list):
        for element in item:
            item_word_count, item_character_count = process_item(element)

            character_count += item_character_count
            word_count += item_word_count

    return word_count, character_count

class Command(BaseCommand):
    help = 'Calculates descriptive statistics for ingested data.'

    def add_arguments(self, parser):
        pass

    @handle_lock
    def handle(self, *args, **options):
        word_count = 0
        character_count = 0

        processed = 0

        latest_point = DataPoint.objects.all().order_by('-pk').first()

        print('LATEST: %d' % (latest_point.pk,))

        current_index = 0

        while current_index < latest_point.pk:
            points = DataPoint.objects.filter(pk__gte=current_index, pk__lt=(current_index + 1000)) # pylint: disable=superfluous-parens

            for point in points:
                properties = point.fetch_properties()

                point_word_count, point_character_count = process_item(properties)

                word_count += point_word_count

                character_count += point_character_count

                processed += 1

                if (processed % 10000) == 0:
                    print('%d, WC: %d, CC: %d (%d / %d)' % (processed, word_count, character_count, point.pk, latest_point.pk,))

            current_index += 1000

        print('%d, WC: %d, CC: %d' % (processed, word_count, character_count))
