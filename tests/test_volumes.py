import os

from disco import Disco

# initalize a disco instance
disco = Disco()

# mount a volume
disco.mount("pond", os.environ["POND"])

# read data in this volume
disco.read("pond://yellow.parquet").show()
