# pylint: disable=no-member, line-too-long

from .models import SentimentTokenSource

def update_data_type_definition(definition):
    to_delete = []

    for key in definition.keys(): # pylint: disable=too-many-nested-blocks
        if 'pdk_sentiment_scores_' in key:
            for token_source in SentimentTokenSource.objects.all():
                if token_source.source_id in key:
                    if key.endswith('.' + token_source.source_id) and (key.endswith('.' + token_source.source_id + '.' + token_source.source_id) is False):
                        definition[key]['pdk_variable_name'] = token_source.source_name
                        definition[key]['pdk_variable_description'] = token_source.source_description
                        definition[key]['pdk_codebook_group'] = 'Passive Data Kit: Content Analysis'

                        ranges = []

                        for potential_label in definition.keys():
                            if potential_label != key and potential_label.startswith(key):
                                label = potential_label[len(key) + 1:]

                                if 'range' in definition[potential_label]:
                                    ranges.append((label, definition[potential_label]['range']))

                        ranges.sort(key=lambda variable: variable[0])

                        definition[key]['pdk_labelled_ranges'] = ranges
                    else:
                        to_delete.append(key)

    for key in to_delete:
        del definition[key]

    all_keys = definition.keys()

    all_keys.sort()

    index = 0

    for key in all_keys:
        if 'pdk_sentiment_scores_' in key:
            definition[key]['pdk_codebook_order'] = index
            definition[key]['pdk_codebook_group'] = 'Passive Data Kit: Content Analysis'

            index += 1
