**network-security-foundations**
This project represents Part 1 of the complete Automation Development training path. The primary objective of this section is to establish a deep, hands-on understanding of networking foundations, protocols, information security, and handling data in JSON format.

The knowledge and tools acquired throughout this phase (such as curl, openssl, dig, and Python) form the essential infrastructure required for root cause analysis (RCA), traffic inspection, and complex API testing in the subsequent stages of the training path.

# Directory structur
network-security-foundations/
  scripts/
    decode_jwt.py
    fernet_demo.py
  docs/
    http_analysis.md
    dns_analysis.md
    tls_analysis.md
    crypto_vs_encoding.md
    json_notes.md
    auth_flows.md
  README.md
  .gitignore
  .env
  pyproject.toml
  main.py
  conftest.py


rerequisites & Tooling
The project is executed and run locally using the following tools:
Python 3.13 (Environment and dependency management handled via uv)
curl - For sending and analyzing HTTP/HTTPS requests
openssl - For inspecting SSL/TLS certificates and cryptographic operations
dig - For querying and analyzing DNS records

# Install dependencies and synchronize the environment
uv sync

# Verifying Tool Availability
curl --version
openssl version
dig -v  # Or nslookup on Windows
uv run python -c "import jwt, cryptography, requests; print('python deps ok')"

# Running the Python Scripts
uv run python scripts/fernet_demo.py

# Running the JWT Decoding and Verification Demo
uv run python scripts/decode_jwt.py

1.What is the difference between HTTP and HTTPS, and what does TLS add?
HTTP represents unsecure web browsing, where anyone can see everything sent in the request. In contrast, HTTPS is secure because it integrates the TLS protocol, which protects the data by encrypting it so that it appears as unreadable characters. It uses asymmetric encryption with a public and private key during the Handshake phase, and later, once it authenticates the communication with the server, it proceeds with symmetric encryption, which is faster. It also goes through the authentication stage to check the certificate, ensuring that it is indeed the real website and that its validity is good.

2.What does a 401 status code mean compared to a 403 status code, and when is each appropriate?
401 is when a request is sent with a wrong password and it doesn't recognize you, so you need to identify yourself. And 403, it recognizes you and knows who you are, but you don't have access to where you are trying to enter.

3.What is the difference between PUT and PATCH?
PATCH is for updating an existing resource, meaning a single field from the resource and all the rest will stay the same. 
PUT is for updating the entire resource from scratch, and whatever you didn't include in the request gets reset.

4.How does DNS resolution work, and what is the difference between a recursive resolver and an authoritative name server?
DNS resolution works in stages until reaching the exact IP address. There is the resolver that manages the entire process. It starts from the Root Server, which redirects to the TLD based on the website's extension, and the TLD redirects to the server where the IP address is located. It is possible that the authoritative server will return a synonym a CNAME record where the IP is located, until the resolver gets the actual IP and saves it for a certain amount of time until that time expires

5.What is the meaning of TTL in a DNS record, and how is it relevant when investigating an issue?
TTL is the time that the IP address is saved in the resolver's memory. It is relevant in troubleshooting in a situation where a server crashes or the website won't load, because I can check at which stage it stopped and see if maybe the IP address is no longer updated. I can clear the resolver's cache, try the request again, and check if that was the issue.

6.What is a certificate chain of trust, and why does a browser trust a certificate?
A browser trusts a certificate based on the Chain of Trust. When a browser validates a certificate, it checks that the expiration date is valid and that today's date falls within the certificate's validity range. It also verifies that the certificate was signed by a trusted Certificate Authority (CA).

The Chain of Trust is a hierarchical structure. The browser has built-in trust for a limited number of Root CAs. When we visit a website, the browser verifies the website's certificate by tracing its signatures up through Intermediate CAs until it reaches a trusted Root CA. If the chain is unbroken and the dates are valid, the browser establishes trus

7.What is the difference between an expired certificate and a self-signed certificate?
An expired certificate is a website that had a signature from a CA for a certain period, and that period ended, so it no longer has approval. In contrast, a self-signed certificate is a certificate that might have a good validity date, but the signature was not made by a secure CA authority.

8.What is the difference between encoding, hashing, and encryption? Provide an example for each.
*Encoding*
Encoding means converting the data format into a format that can be transmitted over the network. For example, converting data to Base64 is one of the formats it understands, and it looks like gibberish.
*Hashing*
Hashing is a one-way function (one-to-one encryption) that cannot be reversed, which is why it is suitable for things like passwords. The real data disappears, and the scrambled characters remain. An example of this is using the SHA-256 algorithm.
*Encryption*
Encryption is a form of masking data that can be decrypted back, but only if you hold the secret key can you decrypt the encrypted code back to its original form. For example, if my text is my secret code and the key is key!@, the output will be gibberish, and to decrypt it back, we will need to use the key key!@.

9.Why is Base64 not considered a security measure?
Since it is ultimately just an encoding that can be decoded using a simple decoding function—without requiring a special key, but simply by running a function to get the original data—it is used only to allow us to transmit data over the network successfully.

10. What is the difference between symmetric and asymmetric encryption, and how does TLS utilize both?
Asymmetric encryption is the encryption that begins when two parties want to communicate securely. It starts with the handshake phase, where they establish a public key that travels over the network and a private key that resides strictly on the server. They agree on an encryption algorithm, which secures the data so that only the server holding the private key can decrypt it.

In contrast, symmetric encryption is the encryption that occurs after this phase. Once I am already connected and the server and client are synchronized, the encryption for all remaining actions is done symmetrically. This works using only a single private key, because this type of encryption is much faster.

TLS is this security protocol that initially operates on asymmetric encryption and then switches to symmetric encryption.


11.Why are passwords stored as hashes rather than being reversibly encrypted?
Because that is part of the security I want to have. Once a user logs in with their credentials, I don't want that information to be stolen, in order to minimize breaches. I don't even provide the option to recover the password; after it undergoes string hashing, it is no longer readable, and that is exactly what I need for security—so that no one can touch it.

The moment that same user logs in again, the hashing function will run once more. If the resulting hash matches what is stored in his database record, the system will recognize it and know which user it is. From that point forward, that's it—the original password is not needed; it is overwritten.

12.What are the three parts that make up a JWT, and what is the role of each part?
*Header*
Tells the server how to handle the token, what type it is, and which algorithm was run on it for the signature.
*Payload*
The part where the data sits, and this is the JSON that contains the information.
*Signature*
It is created by combining the encoded Header and the encoded Payload + a secret key that exists only at the server. They run an algorithm on this in order to check that all the information remained exactly as it is and did not change when it passed through the network

13.Why must you never place sensitive or secret information inside a JWT payload?
The Payload is encoded so that it can be transferred over the network and it is not encrypted, therefore all of its information can be easily retrieved by a simple decode operation. On the other hand, the Signature we talked about is only meant to check if the content arrived whole and that it is not broken, and therefore it still does not encrypt the content and it can be exposed in a moment.

As can be seen in the script – the creation of the server's secret key using the Payload, SECRET, and the HS256 algorithm, and then we receive the token which is a long string divided into 3 parts separated by a dot. The code verifies that the token is indeed divided into 3 parts separated by a dot and that they are all encoded in Base64.

The decoding function basically performs the decode operation – it translates the encoded text using a simple mathematical action without using the secret key at all, proving that the Payload is completely exposed to anyone and is not encrypted.


14.What is the difference between session-based authentication and token-based authentication, and why is a token well-suited for a distributed system?

The difference between a session and a token is that a token works on a Stateless state and the session works on a Stateful state. If I use a distributed system that has a number of computers communicating with each other in a Stateful manner, then the password (session data) is saved in the database of one of the computers and the second one will no longer recognize it. Letting everyone manage a database for this, where everyone saves the exact same data, is wasteful, inefficient, and very expensive. Therefore, the token is excellent for a distributed system because the token is saved with the client and the server will validate it using the secret key it holds, and the key is not expensive to store on all the computers.

15.What test scenarios should be covered for an endpoint that requires authentication?
* Check the validity of the token to ensure it returns a 200 status code.
* Test manipulations for all other scenarios, such as an invalid token, an expired token, or no token at all.
* Verify that after the token is refreshed/replaced, it successfully authenticates using the newly generated token.
* Verify that a regular (standard) permission does not grant access to areas that require administrator permissions.

16. How would you approach investigating an issue where users report that a website is inaccessible? Which tools (curl, dig, openssl) would you use, and in what order?
I will start by using dig to check if it gets stuck during the resolution process. If I receive an IP and everything looks correct, I know DNS is working. If it fails and I don't get an IP, then the failure is at the DNS stage.
Next, I will proceed to openssl to verify if the certificate is valid or if the site lacks a trusted CA signature, causing it to be blocked. If either of these is faulty, the issue is identified.
Otherwise, I will continue to curl and check the returning status code. Based on that, I will determine where the problem lies, whether the site is accessible at all, or if the issue is strictly on the client side