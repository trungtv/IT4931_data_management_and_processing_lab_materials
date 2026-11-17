"""MLlib trên giao dịch tách được: giá cao là BUY, giá thấp là SELL."""

from __future__ import annotations

from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession


def run() -> str:
    spark = SparkSession.builder.appName("trade-side").master("local[1]").getOrCreate()
    try:
        frame = spark.createDataFrame(
            [(30.0, 10, 1.0), (32.0, 8, 1.0), (12.0, 10, 0.0), (11.0, 8, 0.0), (35.0, 5, 1.0)],
            ["price", "quantity", "label"],
        )
        assembled = VectorAssembler(inputCols=["price", "quantity"], outputCol="features").transform(frame)
        model = LogisticRegression(featuresCol="features", labelCol="label", maxIter=20).fit(assembled)
        sample = spark.createDataFrame([(34.0, 6)], ["price", "quantity"])
        predicted = model.transform(
            VectorAssembler(inputCols=["price", "quantity"], outputCol="features").transform(sample)
        ).collect()[0]["prediction"]
    finally:
        spark.stop()
    if predicted != 1.0:
        raise AssertionError(predicted)
    return "BUY"


if __name__ == "__main__":
    print(run())
