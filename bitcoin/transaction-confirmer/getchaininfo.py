from bitcoinrpc import create_rpc_callback

if __name__ == "__main__":
  cb = create_rpc_callback()

  r1 = cb(id="",
          method="getnetworkinfo",
          params=None)

  r2 = cb(id="",
          method="getblockchaininfo",
          params=None)

  print(r1.text)
  print(r2.text)

