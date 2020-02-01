import os
import gzip

def from_text():
  if os.environ["GRAPH_FILE"].endswith(".gz"):
    open_fn = gzip.open
  else:
    open_fn = open

  with open_fn(os.environ["GRAPH_FILE"], "rb") as f:
    for l in f.readlines():
      try:
        inp, oup = l.split()
      except ValueError:
        break
      yield inp, oup
