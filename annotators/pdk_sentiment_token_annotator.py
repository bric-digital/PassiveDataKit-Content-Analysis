# pylint: disable=line-too-long, no-member

from __future__ import print_function

import string

from django.utils.text import slugify

from django.conf import settings

from ..models import SentimentToken

SKIP_FIELD_NAMES = (
    'url',
)

def annotate(content, field_name=None): # pylint: disable=too-many-branches
    if field_name in SKIP_FIELD_NAMES:
        return {}

    score_dictionary = {}

    try:
        score_dictionary = settings.PDK_SENTIMENT_TOKEN_DICTIONARY_CACHE
    except AttributeError:
        for source in list(SentimentToken.objects.all().order_by('source').values_list('source', flat=True).distinct()):
            scores = {}

            for token in SentimentToken.objects.filter(source=source):
                token_value = token.token.lower()

                if (token_value in scores) is False:
                    scores[token_value] = {}

                scores[token_value][token.label] = token.score

            score_dictionary[source] = scores

        settings.PDK_SENTIMENT_TOKEN_DICTIONARY_CACHE = score_dictionary

        print('Sentiment token cache built.')

    scores = {}

    if content is None:
        content = ''

    content = content.lower().strip()

    non_punc = set(string.punctuation)

    for source in score_dictionary.keys():
        source_scores = {}

        for token in score_dictionary[source].keys():
            count = 0

            if content == token:
                count += 1

            if content.startswith(token + ' '):
                count += 1

            if content.endswith(' ' + token):
                count += 1

            if (' ' + token + ' ') in content: # pylint: disable=superfluous-parens
                count += content.count(' ' + token + ' ')

            token_no_punc = ''.join(ch for ch in token if ch not in non_punc).strip()

            if token_no_punc == '':
                count += content.count(token)

            if count > 0:
                for label in score_dictionary[source][token]:
                    if (label in source_scores) is False:
                        source_scores[label] = 0

                    source_scores[label] += count * score_dictionary[source][token][label]

        scores[slugify(source).replace('-', '_')] = source_scores

    annotation_field = 'pdk_sentiment_scores'

    if field_name is not None:
        annotation_field = 'pdk_sentiment_scores_' + field_name

    return {
        annotation_field: scores,
        # 'cleartext': content,
    }
