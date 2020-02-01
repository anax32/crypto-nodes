import requests
import json
import os


def create_rpc_callback():
  url = "http://%s:%s" % (os.environ["RPC_HOST"], os.environ["RPC_PORT"])
  session = requests.Session()

  session.headers.update({"content-type": "text/plain",
                          "cache-control": "no-cache"})
  session.auth=(os.environ["RPC_USER"], os.environ["RPC_PASS"])

  def rpc_callback(id, method, params):
    mparams = []
    for p in params:
      try:
        v = int(p)
      except ValueError:
        v = p

      mparams.append(v)

    str = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": mparams,
            "id": id})

    response = session.post(url, data=str)

    return response

  return rpc_callback


if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="bitcoind RPC caller")
  parser.add_argument("method",
                      default="getblockchaininfo",
                      type=str,
                      nargs=1,
                      help="rpc method; see https://bitcoin.org/en/developer-reference#rpcs")
  parser.add_argument("params",
                      default=None,
                      type=str,
                      nargs=argparse.REMAINDER,
                      help="parameters to the call")
  args = parser.parse_args()

  rpc_callback = create_rpc_callback()

  response = rpc_callback(id="",
                          method=args.method[0],
                          params=args.params)

  print(response.text)
