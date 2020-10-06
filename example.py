from flow.operators.flow import Flow, FlowType
from flow.types.basic import IntType
from flow.types.table import Table, Row
from cloudburst.client.client import CloudburstConnection


def map_fn(self, row: Row) -> int:
    return row["a"] + row["b"]


def filter_fn(self, row: Row) -> bool:
    return row["sum"] % 2 == 0


cloudburst = CloudburstConnection(
    "a7b4fb6f87473467c86de15406e6a094-2079112079.us-east-1.elb.amazonaws.com",
    "34.239.175.232",
)

cloudburst.list()

import random
import string
salt = "".join(random.choices(string.ascii_letters, k=6))

print("Running sanity check")
cloud_sq = cloudburst.register(lambda _, x: x * x, "square-2"+salt)
print(cloud_sq(2).get())
cloudburst.delete_dag("dag")
cloudburst.register_dag("dag", ["square-2"+salt], [])
print(cloudburst.call_dag("dag", {"square-2"+salt: [2]}).get())

# 1 / 0
print("Running example flow")
dataflow = Flow("example-flow"+salt, FlowType.PUSH, cloudburst)
dataflow.map(map_fn, names=["sum"]).filter(filter_fn)

table = Table([("a", IntType), ("b", IntType)])

table.insert([1, 2])
table.insert([1, 3])
table.insert([1, 4])

dataflow.register()
dataflow.deploy()

print(dataflow)
print("deployed")
print(dataflow.run(table).get())