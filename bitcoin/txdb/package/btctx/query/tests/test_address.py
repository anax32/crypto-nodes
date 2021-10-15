import pytest
from mock import patch

from btctx.query import address


from .random_transactions import random_transaction


@patch("btctx.rpc.bitcoind.BitcoinRPC")
def test_getaddressinfo(rpc_mock):
  rpc_mock.return_value = {"txid": "0"}

  address.getaddressinfo("0000", rpc_mock)

  assert rpc_mock.called_with("getaddressinfo", "0000")
  assert rpc_mock.called_with("validateaddress", "0000")
