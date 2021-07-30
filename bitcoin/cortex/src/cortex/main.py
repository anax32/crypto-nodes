"""
FastAPI entrypoint for the cortex blockchain explorer

This handles calling the RPC functions on the node without
exposing the node authentication data to the web client
"""
import os
import sys
import logging


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .bitcoindrpc import BitcoinRPC


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# setup logging
# FIXME: move to logging config file
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter(
        "[%(name)s - %(filename)s:%(lineno)s:%(funcName)s] %(levelname)s - %(message)s"
    )
)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(os.getenv("LOG_LEVEL", "WARN"))


@app.on_event("startup")
def startup_init():
  os.environ["RPC_USERNAME"]
  os.environ["RPC_PASSWORD"]
  os.getenv("RPC_HOSTNAME", "127.0.0.1")
  os.getenv("RPC_PORT", 8332)

  app.state.bnrpc = BitcoinRPC(
    username=os.environ["RPC_USERNAME"],
    password=os.environ["RPC_PASSWORD"],
    host=os.getenv("RPC_HOSTNAME", "127.0.0.1"),
    port=os.getenv("RPC_HOSTPORT", 8332)
  )

  app.state.logger = logger

  info = app.state.bnrpc("getrpcinfo")


@app.get("/", tags=["blockchain"])
def getblockchaininfo(request: Request):
  request.app.state.logger.info("getblockchaininfo")
  return request.app.state.bnrpc("getblockchaininfo")


@app.get("/tip", tags=["blockchain"])
def getbestblockhash(request: Request):
  request.app.state.logger.info("getbestblockhash")
  return request.app.state.bnrpc("getbestblockhash")


@app.get("/block/{blockhash}", tags=["blockchain"])
def getblock(blockhash: str, request: Request):
  request.app.state.logger.info("getblock: '%s'", blockhash)
  return request.app.state.bnrpc("getblock", blockhash, 1)


@app.get("/tx/{txid}", tags=["transactions"])
def getrawtransaction(txid: str, request: Request):
  request.app.state.logger.info("getrawtransaction: '%s'", txid)
  return request.app.state.bnrpc("getrawtransaction", txid, True)


@app.get("/mempool", tags=["mempool"])
def getrawmempool(request: Request):
  request.app.state.logger.info("getrawmempool")
  return request.app.state.bnrpc("getrawmempool", True)


@app.get("/mempool/{txid}", tags=["mempool"])
def get_mempool_entry(txid: str, request: Request):
  request.app.state.logger.info("getmempoolentry: '%s'", txid)
  return request.app.state.bnrpc("getmempoolentry", txid)


@app.get("/node")
def get_node_info():
  pass
