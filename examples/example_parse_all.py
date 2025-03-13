"""PARSING ALL DEMO.

Setup:

    We have files with random text.

Goal:

    We want to extract all regex matches within the file.

"""

import os

from daft import Session

from disco import Disco

# 1. initalize a disco instance
disco = Disco()

# 2. mount a volume which contains the stories
disco.mount("pond", os.environ["POND"])

# 3. read our stories as a text stream
stream = disco.stream("pond://stories/*.txt")

# 4. use a regex to extract anything appearing after 'the'
the_thing_pattern = r"\b(?i:the)\s+(?P<thing>\w+)"

# 5. parse all occurrences and flatten via stream parse_lines
df = stream.parse_all(the_thing_pattern)
df.show()

# 6.5 execute some sql
sess = Session()
sess.create_temp_table("things", df)
sess.sql("""
    SELECT thing, count(*) AS mentions FROM things
    GROUP BY thing
    ORDER BY mentions DESC
""").show()
