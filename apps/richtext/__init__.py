import bleach


# Constants for cleaning richtext html.

REDUCED_ALLOWED_TAGS = ('a', 'b', 'em', 'i', 'strong', 'p', 'u', 'strike',
    'sub', 'sup', 'br')

RICH_ALLOWED_TAGS = REDUCED_ALLOWED_TAGS + ('h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ol', 'ul', 'li', 'hr', 'blockquote',
        'span', 'pre', 'code', 'div', 'img',
        'table', 'thead', 'tr', 'th', 'caption', 'tbody', 'td', 'br')


REDUCED_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
}

RICH_ALLOWED_ATTRIBUTES = REDUCED_ALLOWED_ATTRIBUTES.copy()

RICH_ALLOWED_ATTRIBUTES.update({
    'img': ['src', 'alt', 'style', 'title'],
    'p': ['style'],
    'table': ['align', 'border', 'cellpadding', 'cellspacing',
        'style', 'summary'],
    'th': ['scope'],
    'span': ['style'],
    'pre': ['class'],
    'code': ['class'],
})


RICH_ALLOWED_STYLES = ('text-align', 'margin-left', 'border-width',
    'border-style', 'margin', 'float', 'width', 'height',
    'font-family', 'font-size', 'color', 'background-color')


BLEACH_CLEAN = {
    'default': {
        'tags': REDUCED_ALLOWED_TAGS,
        'attributes': REDUCED_ALLOWED_ATTRIBUTES,
        'styles': [],
        'strip': True,
    },
    'rich': {
        'tags': RICH_ALLOWED_TAGS,
        'attributes': RICH_ALLOWED_ATTRIBUTES,
        'styles': RICH_ALLOWED_STYLES,
        'strip': True,
    },
}


def clean_html(config_name, value):
    if value:
        return bleach.clean(value, **BLEACH_CLEAN[config_name])
    else:
        return value
