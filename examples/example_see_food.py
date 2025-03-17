"""SEE FOOD EXAMPLE.

Setup:

    We will label photos as HOT DOG or NOT HOT DOG.

    - Question for you, what is better the octopus recipe?
    - Answer for you, eight recipes for octopus.

Goal:

    (1) save each image's embeddings to a parquet file.
    (2) produce a new csv with the image path (pk) and its features.

Notes:
    In pure daft, you would list URLs then use URL download.
    Here we are showcasing what a "lazy blob" might look like, which has
    the same functionality as url_download but is hidden from the user.

    Effectively creating a "stream" of lazy blobs with metadata, then
    we chain any transformations and lazily fetch the binary data once
    it is actually needed.
"""

import os

from daft import col

from disco import Disco
from disco.model.__hf import HuggingFaceModel

# 1. initalize a disco instance
disco = Disco()

# 2. mount a volume which contains the food images
disco.mount("pond", os.environ["POND"])

# 3. use the HF model "openai/clip-vit-base-patch32" with zero-shot-classification.
disco.use_model("clip", model=HuggingFaceModel.zero_shot_image_classification("openai/clip-vit-base-patch32"))

# 4. create a daft "classifier" function from the model.
classifier = disco.create_classifier(model="clip", labels=["hot dog", "not hot dog"])

# 5. read the images as a stream then decode into daft Image type
stream = disco.stream("pond://food/10/**/*.jpg").decode("image/jpeg")

# 6. label the images
df = stream.frame().with_column("kind", classifier(col("bytes")))

df.show()
