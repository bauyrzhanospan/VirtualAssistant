import requests
import re
from lxml import html
from lxml.html.clean import clean_html
import glob

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

#url for health = 'https://www.myenglishteacher.eu/blog/at-the-doctor-medical-english-vocabulary-list/'
#url for safety =
#url for entertainment =
#url for energy =
#url for work =
#url for food =
memes = glob.glob('*.html')
for meme in memes:
    with open(meme, "r") as f:
        m = f.read()
        n = []
        m = m.split('<section class="entry clearfix first_letter">', 1 )[1]
        m = m.split('</section>', 1 )[0]
        m = re.compile(r'<li>(.*?)</li>').findall(str(m))
        for line in m:
            n.append(remove_html_markup(str(line).replace("&#8217;", "")))
            name = meme[:5]
            with open(name, 'a') as f:
                f.write(str(remove_html_markup(str(line).replace("&#8217;", ""))) + "\n")