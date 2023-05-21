# crypto_api
REST API for generating valid cryptocurrency addresses and displaying them
Metamask and other software wallets keep private keys on the device.
Under REST API I assume that we have some centralized storage and should have some user database.
So under this assumption I decided to implement JWT authorization so that we can generate multiple addresses for the same user.
