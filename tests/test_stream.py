import os

from disco import Disco

# initalize a disco instance
disco = Disco()

# mount a volume
disco.mount("pond", os.environ["POND"])

# read data with a single column
disco.stream("pond://alice.text").show()

# read data that can be a daft dataframe
disco.stream("pond://yellow.parquet").read().show()

# apply a transformation
disco.stream("pond://alice.text").encode("gzip").show()
