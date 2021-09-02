"""
FastAPI entrypoint for the cortex blockchain explorer

This handles calling the RPC functions on the node without
exposing the node authentication data to the web client
"""
import os
import sys
import logging


from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .bitcoindrpc import BitcoinRPC

from .btc_routes import router as btc_router
from .tx_ui import router as tx_ui_router


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


app = FastAPI()
app.include_router(btc_router)
app.include_router(tx_ui_router)


static_dir = os.path.join(os.path.dirname(__file__), "statics")
app.mount("/static", StaticFiles(directory=static_dir), name="statics")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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
