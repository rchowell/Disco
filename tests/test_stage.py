import os

from disco import Disco

# initalize a disco instance
disco = Disco()

# mount a volume
disco.mount("pond", os.environ["POND"])

# read data with a single column
disco.read("pond://alice.text").stream().show()

# read data with multiple columns
disco.read("pond://yellow.parquet").stream("payment_type").show()

# apply a transformation
disco.read("pond://alice.text").stream().encode("gzip").show()
