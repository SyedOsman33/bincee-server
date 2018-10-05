from django_enumfield import enum


class DeviceTypeEntityEnum(enum.Enum):

    DRIVER = 1
    SCHOOL = 2
    STUDENT = 3

    labels = \
    {
        DRIVER: "Driver",
        SCHOOL: "School",
        STUDENT: "Student",
    }
