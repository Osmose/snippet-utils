# Snippet Bulk Import Script

A utility for making the bulk-import of snippets into the
[home-snippets-server][] a little easier.

[home-snippets-server]: https://github.com/mozilla/home-snippets-server/

## Caveats

* Currently only supports basic snippets.
* Assumes snippet text contains a link.
* Skips failures.
* Assumes that locale Client Match Rules have a description of the form
  `Locale: en-US`.

## Howto

1. Obtain a dump of the Client Match Rules from the server you wish to import
   into. This can be done by logging into the admin interface, navigating to the
   Client Match Rule list, and clicking *Dump Data* in the top right.

2. Visit the [list of all localized snippet strings][localized-snippets] and
   find the string for the snippet you wish to import. The links on that page
   point to JSON files. Copy the link for your string.

3. Obtain a copy of the image that you want to use as the snippet icon. JPEG and
   PNG are supported.

4. Run the script, passing in the name of the snippet, path to the Client Match
   Rule dump, path to the image, url of the l10n JSON, and link to insert into
   the snippet text. Optionally, you can provide the `--extra-rules` argument,
   which takes a list of Client Match Rule IDs and adds them to all imported
   snippets (useful for adding `Firefox: All GA` or channel rules).

Run `bulk_import.py --help` for more information on supported arguments.

## Example

```bash
./bulk_import.py "Test Snippet" ./homesnippets-clientmatchrule.json ./snippet_image.png "http://l10n.mozilla-community.org/~pascalc/langchecker/?action=api&file=snippets.lang&stringid=fakeidthing" "https://mozilla.org" --extra-rules=23 > ./snippets.json
```

Yeah, that's long. But it's way better than importing these by hand.

[localized-snippets]: http://l10n.mozilla-community.org/~pascalc/langchecker/?action=api&file=snippets.lang

## License

Copyright (c) 2012 Michael Kelly

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
