import os
import re
import math
import hashlib
import unicodedata

from django.core.validators import ValidationError, validate_slug
from django.utils.encoding import smart_unicode


# Extra characters outside of alphanumerics that we'll allow.
SLUG_OK = '-_'


def slugify(s, ok=SLUG_OK, lower=True):
    # L and N signify letter/number.
    # http://www.unicode.org/reports/tr44/tr44-4.html#GC_Values_Table
    rv = []
    for c in smart_unicode(s):
        cat = unicodedata.category(c)[0]
        if cat in 'LN' or c in ok:
            rv.append(c)
        if cat == 'Z':  # space
            rv.append(' ')
    new = re.sub('[-\s]+', '-', ''.join(rv).strip())
    return new.lower() if lower else new


def slug_validator(s, ok=SLUG_OK, lower=True):
    """
    Raise an error if the string has any punctuation characters.

    Regexes don't work here because they won't check alnums in the right
    locale.
    """
    if not (s and slugify(s, ok, lower) == s):
        raise ValidationError(validate_slug.message,
                              code=validate_slug.code)


def get_partition_id(pk, chunk_size=1000):
    """
    Given a primary key and optionally the number of models that will get
    shared access to a directory, return an integer representing a directory
    name.
    """
    return int(math.ceil(pk / float(chunk_size)))


def safe_filename(filename):
    """Generate a safe filename for storage."""
    name, ext = os.path.splitext(filename)
    return "%s%s" % (hashlib.md5(name.encode('utf8')).hexdigest(), ext)
