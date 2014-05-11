pybuxfer
========

A simple interface to Buxfer based on their web API, using requests.

See [Buxfer's API page](https://www.buxfer.com/help/api "API Help") for more information about the
Buxfer web API.

Sample Usage
------------
    >>> import buxfer
    >>> b = buxfer.Buxfer('myusername', 'mypassword')
    >>> b.transactions()
    {"status": "OK", "numTransactions": 1334, "transactions": [{
      "key-transaction": {
        "id": "2d510c2696ec50d19a4e122129c455df",
        "description": "RECURRING TRANSFER REF #OPEQG7BT",
        "date": "21 Feb",
        "type": "income",
        "amount": 25,
        "accountId": "eca68525d89d2385dda040c3b5c571c2",
        "tags": "transfer",
      },
      "key-transaction": {
        "id": "45fd72247572d026f165aa5256ffea6b",
        "description": "RECURRING TRANSFER REF #OPE7XXPW",
        "date": "20 Feb",
        "type": "expense",
        "amount": 25,
        "accountId": "eca68525d89d2385dda040c3b5c571c2",
        "tags": "transfer",
      },
      "key-transaction": {
        "id": "bb4871250c00d240de54ed522e9adaf6",
        "description": "other world computing: universal hd adapter (ide/sata : usb 2)",
        "date": "17 Feb",
        "type": "sharedbill",
        "amount": 67.85,
        "accountId": "e7b9d4d7c6974ad1e9ee320ad302874d",
        "tags": "",
        "extraInfo": "This transaction is a shared expense of $67.85, paid by John, split equally between me and John.",
      }
    }]
    }
