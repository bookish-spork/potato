# Copyright 2021 Ryo Nakano

import polib
import glob

files = glob.glob ("./src/*.po")
for file in files:
    po = polib.pofile(file)
    destfile = open(file + ".txt", mode="w")

    for entry in po.translated_entries():
        msgid = entry.msgid
        msgstr = entry.msgstr
        if msgid == msgstr:
            continue

        destfile.write('原文: {}\n筆者訳: {}\n\n'.format(msgid, msgstr))
    
    destfile.close()
