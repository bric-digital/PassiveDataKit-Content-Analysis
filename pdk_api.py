# pylint: disable=no-member, line-too-long

from .models import SentimentTokenSource

def update_data_type_definition(definition):
    to_delete = []

    for key in definition.keys():
        if key.startswith('pdk_sentiment_scores_'):
            for token_source in SentimentTokenSource.objects.all():
                if token_source.source_id in key:
                    if key.endswith('.' + token_source.source_id):
                        definition[key]['pdk_variable_name'] = token_source.source_name
                        definition[key]['pdk_variable_description'] = token_source.source_description
                    else:
                        to_delete.append(key)

    for key in to_delete:
        del definition[key]
