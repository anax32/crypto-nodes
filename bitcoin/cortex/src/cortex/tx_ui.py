import os
import logging

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


from os.path import dirname, join


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/ui",
    tags=["ui"]
)


template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)


@router.get("/")
def home():
  pass


@router.get("/mempool")
def view_mempool(request: Request):
  request.app.state.logger.info("getrawmempool")
  mempool = request.app.state.bnrpc("getrawmempool", True)

  return templates.TemplateResponse("mempool.html", {
      "request": request,
      "mempool": mempool
  })


@router.get("/{txid}")
def view_transaction(txid: str, request: Request):
  request.app.state.logger.info("getrawtransaction: '%s'", txid)
  tx = request.app.state.bnrpc("getrawtransaction", txid, True)
  return templates.TemplateResponse("transaction.html", {
      "request": request,
      "txid": txid,
      "tx": tx
  })
