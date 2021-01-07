##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
# This allows us to generate to keywords.py for PostgreSQL for used by
# qtIdent and qtTypeIdent functions for scanning the keywords type.
#
# In order to generate keywords.py for specific version of PostgreSQL, put
# pg_config executable in the PATH.
#
##########################################################################

import os
import re

if __name__ == '__main__':

    keywords_file = open('keywords.py', 'w')

    keywords_file.write('# ScanKeyword function for snowball admin')
    keywords_file.write('\n\ndef ScanKeyword(key):')
    keywords_file.write('\n    keywordDict = {\n')

    with open("ClickHouseLexer.g4", "rb") as ins:

        keyword_types = [
            u'UNRESERVED_KEYWORD', u'COL_NAME_KEYWORD',
            u'TYPE_FUNC_NAME_KEYWORD', u'RESERVED_KEYWORD'
        ]
        unreserved_keyword=['remote', 'on']

        for line in ins:
            line = line.decode().rstrip().lower()
            # gen reserved keyword
            if line[0:2] == 'k_':
                match = re.findall(r"^k_(.*):.*;", line)
                keywords_file.write("        " +
                                    "'" + ''.join(match) + u"': " +
                                    str(keyword_types.index(
                                        u'RESERVED_KEYWORD')) + ',\n'
                                    )
            # gen column name keyword
            if line[0:2] == 't_':
                match = re.findall(r"^t_(.*):.*;", line)
                keywords_file.write("        " +
                                    "'" + ''.join(match) + u"': " +
                                    str(keyword_types.index(
                                        u'COL_NAME_KEYWORD')) + ',\n'
                                    )
        for w in unreserved_keyword:
            keywords_file.write("        " +
                        "'" + w + u"': " +
                        str(keyword_types.index(
                            u'UNRESERVED_KEYWORD')) + ',\n'
                        )
    keywords_file.write('\n        }\n')
    keywords_file.write(
        '    return keywordDict.get(key, None)')
