CREATE DATABASE IF NOT EXISTS transactions;
USE transactions;

/*
  holds the list of transaction ids
*/
CREATE TABLE IF NOT EXISTS txs (
  txid BIGINT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(txid)
)

/*
  holds the inputs for each transaction
*/
CREATE TABLE IF NOT EXISTS ins (
  inid BIGINT NOT NULL AUTO_INCREMENT,
  txid BIGINT NOT NULL,
  input_txid BIGINT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (txid) REFERENCES txids (txid),
  FOREIGN KEY (input_txid) REFERENCES txids (txid)
)

/*
  holds the addresses used as outputs for a transaction
*/
CREATE TABLE IF NOT EXISTS outs (
  outid BIGINT NOT NULL AUTO_INCREMENT,
  txid BIGINT NOT NULL,
  address BIGINT NOT NULL,
  PRIMARY KEY (outid),
  FOREIGN KEY (txid) REFERENCES txids (txid)
)
