dummy_transactions = {
  "txid": "prev_tx_01",
  "vout": [
    {"value": 1, "n": 0, "scriptPubKey": {"addresses": ["out_01_0000"]}},
    {"value": 2, "n": 1, "scriptPubKey": {"addresses": ["out_01_0001"]}}
  ]
}

random_transaction = [
{
  "txid": "00008d95b8a61dbab1050d19eaaca5a83410a569c2aa6ea3bd3ef0a7cee30d2b",
  "hash": "2154e4851ab25ef6412427a2dfd37f5db8466e288aaf32d09c540dc8d20b1685",
  "version": 1,
  "size": 733,
  "vsize": 541,
  "weight": 2164,
  "locktime": 0,
  "vin": [
    {
      "txid": "prev_tx_01",
      "vout": 1,
      "scriptSig": {
        "asm": "002093082d5280b36fa11aaf1cd573c4c6267b63260a1aaea7a068a54a2f45bc9de6",
        "hex": "22002093082d5280b36fa11aaf1cd573c4c6267b63260a1aaea7a068a54a2f45bc9de6"
      },
      "txinwitness": [
        "",
        "3045022100ca062f6791ef35f49c9df5c87cf2e6144f3efdffdeb9ff3242a35374935efbb502203dce9191c429381039cd948eeaddc6627108c24ef2871056afcfc9dd27c0bed201",
        "304402207b5f0d81736e07afa9d0089ebf962e3dc13beb33f3217a0e64b820a9d18b6b2b022068720d91592d4a511b9dcc59b27d01e142d9729177cc63988113032bc87ef06101",
        "522102dde26d53a1480698d6e1a77dd314ee7aae2bca7ae206e2f2506125c79ef554be2102a91337929de8078f732bc00aac5dc4060937683fa29f6cef3ab1c8660f66828e210321921021dbf62811a438cd390b8f1426c8e108d5df1c12c7232422208c995a5653ae"
      ],
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "value": 0.05025759,
      "n": 0,
      "scriptPubKey": {
        "asm": "OP_HASH160 bfd40e8b3abbdc15c7802e79fa68702afbc613a5 OP_EQUAL",
        "hex": "a914bfd40e8b3abbdc15c7802e79fa68702afbc613a587",
        "reqSigs": 1,
        "type": "scripthash",
        "addresses": [
          "3KBK29bNEp3ZW7Ta3ZYeTdELJvc2bH8oyv"
        ]
      }
    },
    {
      "value": 0.0143,
      "n": 1,
      "scriptPubKey": {
        "asm": "OP_DUP OP_HASH160 0540f2ce40bcddd801e550c2b8ab6cf6e6bdb6c9 OP_EQUALVERIFY OP_CHECKSIG",
        "hex": "76a9140540f2ce40bcddd801e550c2b8ab6cf6e6bdb6c988ac",
        "reqSigs": 1,
        "type": "pubkeyhash",
        "addresses": [
          "1UnBf7xxpvC9jsoEtfwKbYd2kYUuT9FUM"
        ]
      }
    },
    {
      "value": 0.0002,
      "n": 2,
      "scriptPubKey": {
        "asm": "OP_HASH160 9270d1f8e20a8ffc6e1c672e061f7f21fd6ab7b0 OP_EQUAL",
        "hex": "a9149270d1f8e20a8ffc6e1c672e061f7f21fd6ab7b087",
        "reqSigs": 1,
        "type": "scripthash",
        "addresses": [
          "3F3KjSFb128R9JTpHhTzgNWf1LudHSwjXM"
        ]
      }
    }
  ]
}
]
