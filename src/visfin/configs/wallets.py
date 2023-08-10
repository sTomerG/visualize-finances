import os

DUO_DEBT_WALLET = "DUO Schuld"
WBW_SISTER = "WBW (Broertje en Zusjelief)"
WBW_FRIENDS = "WBW (The Ridiculous Seven)"
WBW_DISPUUT = "WBW (Alea Iacta Est)"
CASH_WALLET = "Cash"
ING_WALLET = "ING"
KOOPZEGEL_WALLET = "Koopzegel"
REVOLUT_WALLET = "Revolut"
ASN_WALLET = "ASN"
FIXED_CHARGES_WALLET = "ASN Vaste lasten"
EXPECTED_TAXES_WALLET = "Expected taxes"
DEBIT_WALLET = "Debit"
DUO_INVEST_WALLET = "ASN Beleggen (DUO)"
SPLIT_WALLET = "Uitsplitsen"
INVEST_WALLET = "ASN Beleggen (Persoonlijk)"
CRYPTO_WALLET = "Crypto"
SAVINGS_WALLET = "ASN Spaarrekening"

WALLET_MAPPING = {
    SAVINGS_WALLET: [ING_WALLET],
    DUO_DEBT_WALLET: [DUO_INVEST_WALLET],
    DEBIT_WALLET: [WBW_SISTER, WBW_FRIENDS, WBW_DISPUUT, KOOPZEGEL_WALLET],
    ASN_WALLET: [
        CASH_WALLET,
        SPLIT_WALLET,
        REVOLUT_WALLET,
        FIXED_CHARGES_WALLET,
        EXPECTED_TAXES_WALLET,
    ],
}


INITIAL_BALANCES = {
    DUO_DEBT_WALLET: float(os.environ.get("DUO_DEBT_WALLET", 0)),
    WBW_SISTER: float(os.environ.get("WBW_SISTER", 0)),
    WBW_FRIENDS: float(os.environ.get("WBW_FRIENDS", 0)),
    WBW_DISPUUT: float(os.environ.get("WBW_DISPUUT", 0)),
    CASH_WALLET: float(os.environ.get("CASH_WALLET", 0)),
    ING_WALLET: float(os.environ.get("ING_WALLET", 0)),
    KOOPZEGEL_WALLET: float(os.environ.get("KOOPZEGEL_WALLET", 0)),
    REVOLUT_WALLET: float(os.environ.get("REVOLUT_WALLET", 0)),
    ASN_WALLET: float(os.environ.get("ASN_WALLET", 0)),
    FIXED_CHARGES_WALLET: float(os.environ.get("FIXED_CHARGES_WALLET", 0)),
    EXPECTED_TAXES_WALLET: float(os.environ.get("EXPECTED_TAXES_WALLET", 0)),
    DEBIT_WALLET: float(os.environ.get("DEBIT_WALLET", 0)),
    DUO_INVEST_WALLET: float(os.environ.get("DUO_INVEST_WALLET", 0)),
    SPLIT_WALLET: float(os.environ.get("SPLIT_WALLET", 0)),
    INVEST_WALLET: float(os.environ.get("INVEST_WALLET", 0)),
    CRYPTO_WALLET: float(os.environ.get("CRYPTO_WALLET", 0)),
    SAVINGS_WALLET: float(os.environ.get("SAVINGS_WALLET", 0)),
}

ALL_WALLETS = set(INITIAL_BALANCES.keys())
