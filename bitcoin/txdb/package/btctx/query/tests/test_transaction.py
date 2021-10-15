import pytest
from mock import patch

from btctx.query import transaction


from .random_transactions import dummy_transactions, random_transaction

@patch("btctx.rpc.bitcoind.BitcoinRPC")
@pytest.mark.parametrize("txs", random_transaction)
def test_get_input_addresses(rpc_mock, txs):
  rpc_mock.return_value = dummy_transactions

  iaddr = transaction.get_input_addresses(txs, rpc_mock)

  assert rpc_mock.called
  assert rpc_mock.called_with("getrawtransaction", ["prev_tx_01"])

  assert iaddr is not None
  assert isinstance(iaddr, set)
  assert all([isinstance(x, str) for x in iaddr])
  assert len(iaddr) == 1
  assert iaddr.pop() == "out_01_0001"


@pytest.mark.parametrize("tx", random_transaction)
def test_get_output_addresses(tx):
  addrs = transaction.get_output_addresses(tx, None)
  assert addrs is not None
  assert isinstance(addrs, set)
  assert len(addrs) > 0
