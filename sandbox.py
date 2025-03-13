import os

from disco import Disco

# initalize a disco instance
disco = Disco()

# mount a volume
disco.mount("pond", os.environ["POND"])

# read data as a stream
stream = disco.stream("pond://people/*.gz").decode("gzip")
