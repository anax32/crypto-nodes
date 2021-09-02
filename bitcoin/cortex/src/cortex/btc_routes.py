"""
FastAPI entrypoint for the cortex blockchain explorer

This handles calling the RPC functions on the node without
exposing the node authentication data to the web client
"""
import os
import sys
import logging


from fastapi import APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware

from .bitcoindrpc import BitcoinRPC

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/node", tags=["node"])


@router.get("/", tags=["blockchain"])
def getblockchaininfo(request: Request):
  request.app.state.logger.info("getblockchaininfo")
  return request.app.state.bnrpc("getblockchaininfo")


@router.get("/tip", tags=["blockchain"])
def getbestblockhash(request: Request):
  request.app.state.logger.info("getbestblockhash")
  return request.app.state.bnrpc("getbestblockhash")


@router.get("/block/{blockhash}", tags=["blockchain"])
def getblock(blockhash: str, request: Request):
  request.app.state.logger.info("getblock: '%s'", blockhash)
  return request.app.state.bnrpc("getblock", blockhash, 1)


@router.get("/tx/{txid}", tags=["transactions"])
def getrawtransaction(txid: str, request: Request):
  request.app.state.logger.info("getrawtransaction: '%s'", txid)
  return request.app.state.bnrpc("getrawtransaction", txid, True)


@router.get("/mempool", tags=["mempool"])
def getrawmempool(request: Request):
  request.app.state.logger.info("getrawmempool")
  return request.app.state.bnrpc("getrawmempool", True)


@router.get("/mempool/{txid}", tags=["mempool"])
def get_mempool_entry(txid: str, request: Request):
  request.app.state.logger.info("getmempoolentry: '%s'", txid)
  return request.app.state.bnrpc("getmempoolentry", txid)


@router.get("/node")
def get_node_info():
  pass
