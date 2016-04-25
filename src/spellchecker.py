import glob
import os
import enchant
import os.path
import configparser
import json
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
import sys
from markspelling import MarkSpelling


def errortotalfunct(errortotal, errortotalprev, filename_jsonscore):
    print('Errors in total: ', errortotal)
    if errortotal <= errortotalprev:
        print('Pass. you scored better or equal to the last check')
        with open(filename_jsonscore, 'w') as outfile:
            json.dump(errortotal, outfile)
            return True
    else:
        print('Fail. try harder next time')
        with open(filename_jsonscore, 'w') as outfile:
            # saves errortotal to json file for future use
            json.dump(errortotal, outfile)
            return False


def main():
    directory_self = os.path.dirname(os.path.realpath(__file__))
    directory_root = os.path.dirname(directory_self)

    config = configparser.ConfigParser()
    config.read(os.path.join(directory_self, 'config.ini'))
    defaultconfigfile = config['DEFAULT']

    directory_posts = os.path.join(directory_root, defaultconfigfile['Filestocheckdir'])
    if os.listdir(directory_posts) == []:
        print('No .md files to evaluate')

    filename_jsonscore = defaultconfigfile['Prevscore']
    if not os.path.isabs(filename_jsonscore):
        filename_jsonscore = os.path.join(directory_self, defaultconfigfile['Prevscore'])
    if not os.path.exists(filename_jsonscore):
        print('Please put Prevscore.json in the location of this file.')

    filename_pwl = defaultconfigfile['PWL']
    if not os.path.isabs(filename_pwl):
        filename_pwl = os.path.join(directory_self, defaultconfigfile['PWL'])

    if os.path.exists(filename_pwl):
        print("PWL file exists")
        pwl = enchant.request_pwl_dict(filename_pwl)
    else:
        print("PWL file does not exist")
        sys.exit(2)

    filenameslist = glob.glob(os.path.join(directory_posts, "*.md"))
    wordswrong = open(config['DEFAULT']['Wordswrongfile'], "w+") # Log of incorrectly spelt words
    filecheck = open(config['DEFAULT']['Filecheck'], "w+") # Log of files that were checked

    errortotalprev = 0
    if os.path.exists(filename_jsonscore):
        with open(filename_jsonscore, 'r') as scorefile:
            errortotalprev = json.load(scorefile)
    spellcheck = SpellChecker("en_GB", filters=[URLFilter, EmailFilter])
    mspell = MarkSpelling(directory_posts, spellcheck, pwl, filecheck, wordswrong, errortotalprev)
    errortotal = mspell.checkfilelist(filenameslist)
    passed = errortotalfunct(errortotal, errortotalprev, filename_jsonscore)
    filecheck.close()
    wordswrong.close()
    if not passed:
        sys.exit(1)


if '__main__' == '__main__':
    main()
