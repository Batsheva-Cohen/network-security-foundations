
**Encoding:**
Encoding is taking information and converting it into a certain format so that additional systems can receive and understand it, for example, transferring data between different communication protocols; it is possible that the information will need to pass in a certain format so that it can pass without problems.

**Encryption:**
Encryption is taking information, encrypting it, it will look like text that is impossible to understand, and it will be possible to decrypt back to the original text only with the help of the key; whoever holds the key will be able to decrypt again, they use this when they want to transfer information from one to another in an encrypted way so that not everyone can take the information, like transferring credit card data.

**Hashing:**
Hashing is like encryption but impossible to decrypt, the original text disappears and it is impossible to restore after the hashing, it is a scrambling of the text into text that looks like gibberish, they use this for passwords for example when I want to save the password by encryption but I have no need to restore it... I authenticate the user once with their password and that's it, the original password disappears and it is impossible to steal it.

**Why Base64 is not a security measure:**
For it to be a security measure, I need it to be confidential, and only someone with authorization should be able to decrypt it. If I took information and performed Base64 on it, I turned this information into a format that can be understood between two parties that communicate with each other and transfer it to one another. Anyone can come and decode this encoding; I do not need a key, and therefore it is not confidential. Hence, it is impossible to use this for security purposes because it is not secured in this manner.

**Asymmetric Encryption**
Asymmetric encryption is encryption that encrypts secret information, managing the encryption with 2 keys: a public key for encryption – everyone can encrypt because it is public and known to everyone, but for decryption there is a private key that is held by only one person and it does not pass, it works on the TLS protocol and is used for encryption and maintaining privacy when browsing websites.

**Symmetric Encryption**
Symmetric encryption is encrypting information with a single key that passes between whoever needs access to the original information, needing the key both for encryption and for decryption, they use it after the asymmetric encryption – I connected to the website I wanted with the help of the asymmetric encryption, when I am already inside the website and everything went well, the browser and the server switch to symmetric encryption, every action I do inside the website is already under symmetric encryption, for example making a backup of some content etc.


**Why is hashing used for password encryption and not reversible encryption?**
Hashing is one-way, it scrambles information and the original information cannot be returned, it is overwritten, and therefore for the purpose of protecting a password I need to use a HASH. I encrypt the information, meaning by a scrambling function that cannot be restored, and thereby prevent the theft of the password. After the user is identified with their password, the scrambling token is saved; when they log in again, then once again the same function is activated, if the output is identical to the saved token they will log in again, and therefore the original password is overwritten every time and is impossible to breach.

If we were to use reversible encryption – there would be a way to restore the original password using a key, and I have absolutely no need for that, and thereby I reduce the risks of theft and save all the security under key management.