#!/usr/bin/env python3

import pathlib
import polib
from google.cloud import translate

def translate_text(text):
    response = client.translate_text(
        request={
            'parent': parent,
            'contents': [text],
            'mime_type': 'text/plain',
            'source_language_code': 'en-US',
            'target_language_code': 'ja',
        }
    )

    return response.translations[0].translated_text

client = translate.TranslationServiceClient()
project_id = 'po-to-txt' # Set your project id
parent = f'projects/{project_id}/locations/global'

print('Checking .po files…\n')

po_dir = pathlib.Path('./submodule')
files = po_dir.glob ('./**/po/**/ja.po')
for file in files:
    print('Target file found: {}'.format(file))
    po = polib.pofile(file)

    path_elements = file.parts
    # ja.po is in subdirectory
    if path_elements[3] != 'ja.po':
        dest_path = 'dest/{}-{}-ja.txt'.format(path_elements[1], path_elements[3])
    else:
        dest_path = 'dest/{}-ja.txt'.format(path_elements[1])

    print('Writing to {}…'.format(dest_path))
    destfile = open(dest_path, mode='w')

    for entry in po.translated_entries():
        msgid = entry.msgid
        msgstr = entry.msgstr
        if msgid == msgstr:
            continue

        gtrans_translated = translate_text(msgid)

        if entry.msgid_plural != '':
            destfile.write('原文（単数形）：{}\n原文（複数形）：{}\n筆者訳：{}\nGoogle翻訳：{}\n\n'.format(msgid, entry.msgid_plural, entry.msgstr_plural[0], gtrans_translated))
        else:
            destfile.write('原文：{}\n筆者訳：{}\nGoogle翻訳：{}\n\n'.format(msgid, msgstr, gtrans_translated))

    destfile.close()

print('\nDone.')
