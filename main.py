from sklearn import datasets
from core import GenAlgorithm

iris = datasets.load_iris()
points = iris.data
ga = GenAlgorithm(
    points,
    cluster_count=5,
    population_size=50,
    steps=10
)
result = ga.run()
