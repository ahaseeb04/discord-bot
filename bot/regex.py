course_regex = "".join((
    "^(?:(?P<faculty>[a-z]{2})\s)?"
    "(?:(?P<department>[a-z]{2,4})\s?(?P<course>[0-9]{4}))+"
    "(?:\s(?P<session>[a-z]{2})\s?(?P<year>[0-9]{4}))?$"
))

course_list_regex = "".join((
    "^(?:(?P<faculty>[a-z]{2})\s)?"
    "(?:(?P<department>[a-z]{2,4}))+"
    "(?:\s(?P<session>[a-z]{2})\s?(?P<year>[0-9]{4}))?$"
))