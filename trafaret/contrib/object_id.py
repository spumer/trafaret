from bson.objectid import ObjectId
from bson.errors import InvalidId

from .. import Trafaret, str_types


class MongoId(Trafaret):
    """ Trafaret type check & convert bson.ObjectId values
    allow_blank: if False it won't generate new ObjectId from None value.

    >>> MongoId()
    <MongoId>
    >>> MongoId(allow_blank=True)
    <MongoId(blank)>
    >>> MongoId().check("5583f69d690b2d70a4afdfae")
    ObjectId('5583f69d690b2d70a4afdfae')
    >>> MongoId(allow_blank=True).check(None)
    ObjectId('5583f6e9690b2d70a4afdfaf')
    >>>extract_error(MongoId(), "just_id")
    "'just_id' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
    """

    convertable = str_types + (ObjectId,)
    value_type = ObjectId
    allow_blank = False

    def __init__(self, allow_blank=False):
        self.allow_blank = allow_blank

    def __repr__(self):
        return "<MongoId(blank)>" if self.allow_blank else "<MongoId>"

    def converter(self, value):
        try:
            return self.value_type(value)
        except InvalidId as e:
            self._failure(str(e))

    def check_and_return(self, value):
        if not self.allow_blank and value is None:
            self._failure("blank value is not allowed")
        if isinstance(value, self.convertable) or value is None:
            return value

        self._failure('value is not %s' % self.value_type.__name__)
