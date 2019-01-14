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
            TRUE = "True"
            FALSE = "False"

        @skip
        class P(Enum):
            A = "A"
            B = "B"
