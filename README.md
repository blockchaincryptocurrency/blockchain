# Python Real Cryptocurrency Blockchain

A complete, educational cryptocurrency implementation in Python.

## Features

- **Blockchain ledger**: Chain of blocks, proof-of-work mining
- **Digital signatures**: Secure transactions (ECDSA)
- **Wallet management**: Key generation, import/export, address validation
- **Transaction handling**: Signed transfers, balance checks
- **Persistence**: Chain, wallets, balances, transaction pool, peers saved to disk
- **Networking**: Peer-to-peer block and transaction propagation, chain sync, fork resolution
- **CLI interface**: Manage wallets, send coins, mine, connect nodes

## File Structure

- `blockchain.py` — Blockchain logic, mining, validation, persistence
- `wallet.py` — Key generation, signing, address management
- `network.py` — Peer-to-peer communication, sync, propagation
- `cli.py` — Command-line interface for all operations
- `utils.py` — Hashing and pretty-print helpers

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/blockchaincryptocurrency/blockchain.git
   cd blockchain
   ```

2. **Install requirements**
   ```bash
   pip install ecdsa argparse
   ```

## Usage

### 1. Create a wallet
```bash
python cli.py create-wallet
```
Wallet files are saved in the `wallets/` directory.

### 2. Import a wallet
```bash
python cli.py import-wallet <address>
```

### 3. Check balance
```bash
python cli.py balance <address>
```

### 4. Send coins (signed transaction)
```bash
python cli.py send <from_addr> <to_addr> <amount>
```
Requires sender’s wallet file in `wallets/`.

### 5. Mine a block
```bash
python cli.py mine <miner_addr>
```
Mining adds a reward transaction to the block.

### 6. Start a networking server (node)
```bash
python cli.py server <host> <port>
```
Example: `python cli.py server 127.0.0.1 5000`

### 7. Connect to a peer
```bash
python cli.py connect <host> <port>
```
Example: `python cli.py connect 127.0.0.1 5001`

### 8. Sync chain with peer
```bash
python cli.py sync <host> <port>
```
Example: `python cli.py sync 127.0.0.1 5001`

## How it works

- **Wallets**: Generated using ECDSA, saved locally, used to sign transactions.
- **Transactions**: Must be signed with sender’s private key; nodes verify signatures before accepting.
- **Mining**: New blocks are mined via Proof-of-Work; miner receives a reward.
- **Persistence**: Chain, balances, wallets, peers, and pending transactions are stored on disk.
- **Networking**: Nodes broadcast and receive blocks/transactions; adopt the longest valid chain.

## Security & Limitations

- This project is **educational** — not for production or financial use.
- Security: Transactions are cryptographically signed, but no encryption of peer-to-peer traffic.
- No global peer discovery; add peers manually.
- No advanced consensus, smart contracts, or DDoS protection.
- Data is stored in local files (not a distributed database).

## Extending

- Add REST/web interface (Flask, FastAPI)
- Add encrypted peer communication
- Upgrade to persistent database (SQLite, LevelDB)
- Implement smart contracts or tokens
- Add peer discovery and NAT traversal

## License

MIT (or specify your preferred license)

---

**This repository demonstrates all core principles of a real cryptocurrency system in Python.**