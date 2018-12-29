import os
from premailer import transform


def apply_html_style(strhtmltablelist,
                     title='Data Reports',
                     cssfile='tohtmlstyle_example.css'):
    cs = os.path.join(os.path.dirname(__file__), 'views', cssfile)
    with open(cs, 'r', encoding='utf-8') as f:
        css = f.read()
    title = '<div class="tabletitle">'+title+'</div>'
    body = ''.join(strhtmltablelist)
    body = body.replace('class="dataframe"', 'class="GenericTable"')
    res = ''.join([
        '<html><head><style>',
        css,
        '</style></head><body>',
        title,
        body,
        '</body>'
    ])
    return transform(res)
