#!C:\Users\Vincent\PycharmProjects\dj_webservice\dj_webservice\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'spyne==2.12.16','console_scripts','sort_wsdl'
__requires__ = 'spyne==2.12.16'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('spyne==2.12.16', 'console_scripts', 'sort_wsdl')()
    )
