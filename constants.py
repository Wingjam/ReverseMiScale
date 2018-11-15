class Immutable(type):

    def __call__(*args):
        raise Exception("You can't create instance of immutable object")

    def __setattr__(*args):
        raise Exception("You can't modify immutable object")


class AD_TYPES(object):

    __metaclass__ = Immutable

    COMPLETE_LOCAL_NAME = 9
    SERVICE_DATA = 22
    MANIFACTURER = 255

class UNITS(object):

    __metaclass__ = Immutable

    JIN = "jin"
    LBS = "lbs"
    KG = "kg"
    UNKNOWN = "unknown"

