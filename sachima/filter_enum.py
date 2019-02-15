from aenum import Enum, unique, skip


class FilterEnum(Enum):
    @skip
    class TYPE(Enum):
        DATE = "DatePicker"
        DATERANGE = "RangePicker"
        ITEMSELECT = "Select"

    @skip
    class PROPS(Enum):
        @skip
        class SIZE(Enum):
            SMALL = "small"
            BIG = "big"

        @skip
        class MODE(Enum):
            TAGS = "tags"
            MULTIPLE = "multiple"

        @skip
        class ALLOWCLEAR(Enum):
            TRUE = True
            FALSE = False

        @skip
        class SHOWTIME(Enum):
            TRUE = True
            FALSE = False

        @skip
        class DEFAULTOPEN(Enum):
            TRUE = True
            FALSE = False

        @skip
        class OPEN(Enum):
            TRUE = True
            FALSE = False

        @skip
        class LOADING(Enum):
            TRUE = True
            FALSE = False

        @skip
        class SHOWSEARCH(Enum):
            TRUE = True
            FALSE = False
