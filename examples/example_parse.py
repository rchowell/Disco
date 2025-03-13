"""TEXT LOGS DEMO.

Setup:

    We have compressed nginx access logs.

Goal:

    We want to count the number of times each URL was visited.

"""

import os

from daft import Session, col

from disco import Disco

# 1. initalize a disco instance
disco = Disco()

# 2. mount a volume which contains the stories
disco.mount("pond", os.environ["POND"])

# 3. read our stories as a text stream
stream = disco.stream("pond://logs/*.access.log")

# 4. use a regex with matching groups to produce columns
nginx_access_log_pattern = r'(?P<ip>\S+) - (?P<remote_user>\S+) \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<url>[^"]*) HTTP/(?P<http_version>\d\.\d)" (?P<status>\d+) (?P<body_bytes_sent>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'

# 5. extract the url via stream parse_lines
df = stream.parse_lines(nginx_access_log_pattern)

# 6. count unique urls visited using df apis
df.groupby("url").agg(col("url").count().alias("requests")).sort("requests", desc=True).collect().show()

# 6.5 execute some sql
sess = Session()
sess.create_temp_table("logs", df)
sess.sql("""
    SELECT url, count(*) AS requests FROM logs
    GROUP BY url
    ORDER BY requests DESC
""").show()
