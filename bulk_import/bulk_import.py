#!/usr/bin/env python
"""
Bulk import utility for the Firefox Snippets Service.
"""
import argparse
import base64
import jinja2
import json
import re
import sys

import requests


parser = argparse.ArgumentParser(description=globals()['__doc__'],
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('name', help='Display name for the snippet.')
parser.add_argument('client_match_rules', type=file,
                    help='Path to JSON dump of Client Match Rules from the '
                         'server you want to import into.')
parser.add_argument('image', help='Path to image to use as the snippet icon.')
parser.add_argument('l10n_url', help='URL to JSON of localized strings.')
parser.add_argument('link', help='Link to use in snippet.')
parser.add_argument('--extra-rules', type=int, nargs='+',
                    help='Extra Client Match Rule IDs to be attached to '
                         'snippets (e.g. for adding `All GA` rule).')


env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader('./'))


def base64img(filename):
    if filename.endswith('png'):
        mimetype = 'image/png'
    elif filename.endswith(('jpg', 'jpeg')):
        mimetype = 'image/jpeg'
    else:
        return ''

    with open(filename, 'r') as f:
        data = base64.encodestring(f.read())
    return 'data:%s;base64,%s' % (mimetype, data)


class SnippetBulkImporter(object):
    template = env.from_string("""
    <!--basic-->
    <div class="snippet">
      <!--icon:{{ image_url }}-->
      <img class="icon" src="{{ image_b64 }}" />
      <p>{{ text }}</p>
    </div>
    """)

    def __init__(self, name, client_match_rules, image, l10n_url, link,
                 l10n_rule_format=r'Locale: ([a-zA-Z\-]+)', extra_rules=None):
        self.name = name
        self.client_match_rules = client_match_rules
        self.image = image
        self.image_b64 = base64img(image)
        self.link = link
        self.extra_rules = extra_rules

        # Load strings
        response = requests.get(l10n_url)
        self.translations = response.json.values()[0]

        # Store map of locales to id of their client-match rule.
        self.locale_rules = {}
        l10n_re = re.compile(l10n_rule_format)
        for rule in client_match_rules:
            desc = rule['fields']['description']
            match = l10n_re.match(desc)
            if match:
                self.locale_rules[match.group(1)] = rule['pk']

    def get_snippet_code(self, locale):
        try:
            text = self.translations[locale] % self.link
        except TypeError:
            print >> sys.stderr, u'Error in locale <{0}>, skipping: {1}'.format(
                locale, self.translations[locale])
            return None

        return self.template.render({
            'image_url': '',
            'image_b64': self.image_b64,
            'text': jinja2.Markup(text)
        })

    def get_snippet_fixture(self, locale):
        if not locale in self.locale_rules:
            print >> sys.stderr, ('Error: No locale rule found for locale '
                                  '<{0}>. Skipping.'.format(locale))
            return None

        code = self.get_snippet_code(locale)
        if code is None:
            return None

        rules = [self.locale_rules[locale]] + (self.extra_rules or [])
        return {
            'pk': None,
            'model': 'homesnippets.snippet',
            'fields': {
                'body': code,
                'disabled': True,
                'name': ' '.join([self.name, locale]),
                'priority': 0,
                'pub_start': None,
                'pub_end': None,
                'preview': False,
                'client_match_rules': rules
            }
        }

    def get_all_snippet_fixtures(self):
        fixtures = []
        for locale in self.translations.keys():
            fixture = self.get_snippet_fixture(locale)
            if fixture is not None:
                fixtures.append(fixture)
        return fixtures


if __name__ == '__main__':
    args = parser.parse_args()
    client_match_rules = json.loads(args.client_match_rules.read())
    importer = SnippetBulkImporter(args.name, client_match_rules, args.image,
                                   args.l10n_url, args.link,
                                   extra_rules=args.extra_rules)
    fixtures = importer.get_all_snippet_fixtures()
    print json.dumps(fixtures)
