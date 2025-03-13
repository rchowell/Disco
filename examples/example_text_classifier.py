"""TEXT CLASSIFICATION DEMO.

Setup:

    We have a set of pizza reviews (several csv files) with a message and rating.

Goal:

    We must classify (label) each review with 'happy', 'neutral', or 'bad'.

"""

import os

from daft import col

from disco import Disco
from disco.model.__hf import HuggingFaceModel

# 1. initalize a disco instance
disco = Disco()

# 2. mount a volume
disco.mount("comments", os.environ["POND"] + "/comments")

# 3. use the HF model "facebook/bart-large-mnli" with zero-shot-classification.
disco.use_model("bart", model=HuggingFaceModel.zero_shot_classification("facebook/bart-large-mnli"))

# 3.5 create a daft "classifier" function from the model.
classifier = disco.create_classifier(model="bart", labels=["happy", "neutral", "sad"])

# 4. read the reviews from a csv
df = disco.read("comments://pizza_reviews.csv")

# 5. classify each review, appending a 'sentiment' column.
df = df.with_column("sentiment", classifier(col("message")))

# 6. write the csv (or show)
df.show()
