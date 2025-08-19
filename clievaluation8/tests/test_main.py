from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession

from dab_workshop_2025 import main

SparkSession.builder = DatabricksSession.builder
SparkSession.builder.getOrCreate()


def test_main():
    taxis = main.get_taxis()
    assert taxis.count() > 5
