## 1. Valid Certificate Analysis
* **Tested Website URL:** https://badssl.com
* **Subject** badssl.com.*
* **Issuer:** Let's Encrypt
* **Validity Period:** From May 26, 2026, to August 24, 2026

### Field Explanations:
**Subject:** The domain name that the certificate is designated to protect. The asterisk (`*`) indicates that this is a Wildcard certificate, which covers the main domain as well as all of its subdomains.
**Issuer:** The Certificate Authority that verified the website and digitally signed the certificate. In this case, it is the well-known organization Let's Encrypt.
**Validity Period:** The timeframe during which the certificate is considered legally valid. If we attempt to access the website even one day after August 24, 2026, the browser will block the connection immediately.

## 2. Failed TLS Scenarios

### A. Expired Certificate Scenario
**Tested Website URL:** https://expired.badssl.com
**Browser Behavior:** The browser blocks access to the site and displays a security warning page.
**Error Code:** net::ERR_CERT_DATE_INVALID
* **Subject** badssl.com.*
* **Issuer:** Let's Encrypt

### Explanation:
This error occurs because the browser validation checks the certificate's validity dates against the current system time. As seen in the certificate details, this certificate was only valid from **April 9, 2015, to April 13, 2015**. Since we are currently in **2026**, the certificate has expired long ago. Browsers strictly reject expired certificates to prevent users from connecting to unmaintained or potentially hijacked servers. The missing organization fields are standard for Domain Validation certificates and are not the cause of this failure.


# 3. Failed TLS 

### A. Expired Certificate Scenario
**Tested Website URL:** https://self-signed.badssl.com
**Browser Behavior:** The browser blocks access to the site
**Error Code:** net::ERR_CERT_AUTHORITY_INVALID
* **Subject** badssl.com.*
* **Issuer:** badssl.com.*

### Explanation:
The request to browse the website is rejected because the signing entity does not exist in the list of approved CA organizations authorized to sign. Therefore, even though the certificate's validity date is valid, but the Subject and Issuer are signed with badssl.com.* they are the ones who signed the website—and therefore TLS blocked the access because they are not a verified entity in the Root CAs.

The difference between it and a certificate issued by a CA is that for a website with a valid certificate, the signing was not performed by the website itself, but rather by authorized signing entities found in the Root CA. Therefore, if the website (Subject) and the organization (Issuer) are identical, there is no secure and verified signature, and TLS will block the request to browse such a site—even if its validity period is completely valid.

### The Two Promises of TLS:

**Encryption:** This is the agreement established between the server and the client during the handshake. They agree on an encryption method using well-known algorithms. They exchange a Public Key over the network to initialize secure communication, where data is encrypted using this public key. The server is the only one that can decrypt and read these confidential details using its Private Key, which exists strictly on the server side.

**Authentication:** This is performed via the digital certificate issued by a CA. The browser verifies the digital signature against its built-in list of trusted authorities (Root CAs). Only if a valid signature from an authorized root entity exists, can I know with absolute certainty that I am connecting to the correct, legitimate website and not an impersonator.


 ### TLS Tests to be Performed by the QA Tester
1. Certificate Validity and Authentication: It must be checked that the validity date of the digital certificate has not expired and that the system time approves it. Additionally, it must be verified that the certificate truly belongs to one of the approved entities in the CA, without a self-signature.
2. Protocol Version: It must be verified that the server implements and enforces the use of the most updated and secure protocol version—TLS 1.3. A negative test must also be performed to ensure that the server completely blocks and refuses to establish connections that use old versions.
3. Cipher Suite Strength: It must be verified that the encryption algorithms the server chooses to use during the handshake process are strong, modern, and secure algorithms adapted to the requirements of TLS 1.3.

