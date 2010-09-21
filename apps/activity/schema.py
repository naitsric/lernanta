from django.utils.translation import ugettext as _

class UnknownActivityError(Exception):
    """Can't find a specified activity verb or object-type."""

    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)


class Type(object):
    """Represent an entity defined in Atom Activity Base Schema."""

    past_tense = None
    ns = 'http://activitystrea.ms/schema/1.0/'
    
    def __init__(self, name, past_tense=None):
        self.abbrev_name = name
        self.name = "%(namespace)s/%(name)s" % {
            'namespace': self.ns,
            'name': name
        }
        self.past_tense = past_tense

    @property
    def human_readable(self):
        """Generate a human readable form of this type."""
        term = self.name.split('/')[-1]
        if '-' in term:
            return ' '.join(map(lambda s: s.capitalize(), term.split('-')))
        return term.capitalize()

    def __eq__(self, other):
        return self.name == other or self.abbrev_name == other
            
class DerivedType(Type):
    """Represent an entity defined by this site. Should extend a base type."""
    
    ns = 'http://drumbeat.org/activity/schema/1.0'

    def __init__(self, name, parent, past_tense=None):
        super(DerivedType, self).__init__(name, past_tense)
        self.parent = parent

# a list of object-types defined in the activity schema
type_names = [
    'article', 'audio', 'bookmark', 'comment', 'file', 'folder', 'group',
    'note', 'person', 'photo', 'photo-album', 'place', 'playlist', 'product',
    'review', 'service', 'status', 'video', 'event', 'song'
]
object_types = {}
for name in type_names:
    object_types[name] = Type(name)

# a list of verbs defined in the activity schema
verbs = {
    'favorite':    Type('favorite', past_tense=_('favorited')),
    'follow':      Type('follow', past_tense=_('started following')),
    'like':        Type('like', past_tense=_('liked')),
    'make-friend': Type('make-friend', past_tense=_('friended')),
    'join':        Type('join', past_tense=_('joined')),
    'play':        Type('play', past_tense=_('played')),
    'post':        Type('post', past_tense=_('posted')),
    'save':        Type('save', past_tense=_('saved')),
    'share':       Type('share', past_tense=_('shared')),
    'tag':         Type('tag', past_tense=_('tagged')),
    'update':      Type('update', past_tense=_('updated')),
    'rsvp-yes':    Type('rsvp-yes', past_tense=_('is attending')),
    'rsvp-no':     Type('rsvp-no', past_tense=_('is not attending')),
    'rsvp-maybe':  Type('rsvp-maybe', past_tense=_('might be attending')),
}

# Custom types 
object_types.update({
    'project':  DerivedType('project', object_types['group']),
})

# Custom verbs
verbs.update({
    'create':      DerivedType('create',
                               verbs['post'],
                               past_tense=_('created')),
})
