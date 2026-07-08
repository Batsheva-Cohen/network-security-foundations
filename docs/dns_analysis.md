//מחקר וניתוח פרוטוקול DNS

### command
dig leetcode.com A
WHEN: Mon Jun 29 13:39:49 
The answer was received at the date and time specified above

leetcode.com.           300     IN      A       172.66.154.160
leetcode.com.           300     IN      A       104.20.41.79

The website's IP address split into 2 in order to prevent load issues
It is of type A, which converts my domain to its IP
TTL = 300 => The website address will sit in the resolver's temporary memory for 300 seconds; after that, if the request is made again, they will need to import its IP through the series of servers that must be passed

### comand
dig leetcode.com A
Exactly the same website address at a different time
WHEN: Mon Jun 29 13:39:49 

leetcode.com.           280     IN      A       172.66.154.160
leetcode.com.           280     IN      A       104.20.41.79

The TTL time is 280, it sat in the temporary memory, meaning when the address needed to be converted to IP, there was no need to do the whole round trip, rather it sat in the temporary memory and the TTL updated to the time remaining for it to sit there
When this time expires, it will make the whole way again until I get the IP, and it too will sit in the memory for a limited time...


### comand 
dig google.com +trace
**Step-by-Step Resolution Process:*

;; Received 525 bytes from 192.168.1.1#53(192.168.1.1) in 51 ms
Received 525 bytes in response to the request, containing all available root zone servers.

com.                    86400   IN      DS      19718 13 2 8ACBB0CD28F41250A80A491389424D341522D946B0DA0C0291F2D3D7 71D7805A
com.                    86400   IN      RRSIG   DS 8 1 86400 20260712170000 20260629160000 54393 . htlD4gjryEhu5I2+NGVwk8M1NFJAudoKlRjG/Lc6AmbFUhs2X4lXI4u3 sQciCEQPwiN10wuRlT6SCR5f80rhnbPp7vQ/KXSorSEr7qk0pWu9xtXD SJfxqLaiwkuSzQKSdJ4+GGBP6DCAD9rVFrLWZORhMEQn8qxCCcfmsyrK VaKVTzVeGlBDebSbvdDcYs6gA+UQAUQswtm7JXZOsrNnNXxzb1TNjOCp z3ECj6rSAFQ5dXFKCWOTb29+Bb9wOYDvJwAjtAEv6qY0nFOTpzJp4Zcs L5AEGC+NKb6lPsCSqsUtYtOS74wDQOEO0Z9deADQiPr0vRrf/sHBpPa2 BaqGLw==
;; Received 1170 bytes from 198.41.0.4#53(a.root-servers.net) in 128 ms
The root server returned the authoritative servers for the .com TLD (Top-Level Domain) and referred the query to them. The server that handled this request was a.root-servers.net, and it took 128 ms.


;; Received 644 bytes from 192.5.6.30#53(a.gtld-servers.net) in 136 ms
Received a 644-byte response from the TLD server, containing the available authoritative name servers that hold the records for the domain (google.com).


;; Received 55 bytes from 216.239.34.10#53(ns2.google.com) in 114 ms
The authoritative Name Server (NS) that finally returned the actual IP address is ns2.google.com.

### command
dig google.com MX

;; ANSWER SECTION:
google.com.             300     IN      MX      10 smtp.google.com.

;; Query time: 69 msec
;; SERVER: 192.168.1.1#53(192.168.1.1) (UDP)
;; WHEN: Wed Jul 08 10:32:52 ;; MSG SIZE  rcvd: 60

The MX record specifies the mail servers responsible for receiving email messages on behalf of the domain. 
What I learn from this is that when someone sends an email to `user@google.com`, the sending mail server performs a DNS lookup for the MX record of `google.com` to find the exact destination server (`smtp.google.com.`) and the priority number (10 - where a lower number means higher priority)


### What I learn from NS and MX
1. **Separation of Services:** DNS allows us to route traffic to different physical servers based on the *type* of request. Regular web traffic (HTTP/HTTPS) goes to the IP specified in the **A record**, while email traffic goes to the mail server specified in the **MX record**. They do not have to sit on the same machine!
2. **High Availability and Redundancy:** By defining multiple **NS records** (like ns1, ns2, ns3), the domain ensures that its "address book" is always available. Even if one DNS server undergoes maintenance or crashes, backup servers take over instantly, preventing a global outage of the service.

### command -
dig www.terminalx.com
WHEN: Mon Jun 29 13:40:10

;; ANSWER SECTION:
www.terminalx.com.      559     IN      CNAME   ion.terminalx.com.edgekey.net.
ion.terminalx.com.edgekey.net. 21559 IN CNAME   e4881.a.akamaiedge.net.
e4881.a.akamaiedge.net. 20      IN      A       184.31.163.87

**Step-by-Step Resolution Process:**
he request moved between the servers. It started at the Root server and moved to the TLD server. The TLD server returned the address of the NS (Name Server) that manages this domain. 

The Resolver approached the NS, but it could not return the IP address immediately because the requested domain is an alias (CNAME). Instead, it redirected us to a new server with a new address: `ion.terminalx.com.edgekey.net`. 

Then, the `edgekey` server responded that this too is an alias, returning the CNAME: `e4881.a.akamaiedge.net`. Finally, when approaching the `akamaiedge` server, I received the exact IP address from it (`184.31.163.87`).


### The Difference Between A and CNAME Records:

**A Record:** Its role is to connect a domain name to an exact IP address that will be passed to the client in order to display the requested website.
**CNAME Record:** This record's role is to provide a new address for a new server where the IP is located. This process can take several cycles, where each time a CNAME is returned, and we navigate between servers until they finally provide the IP.


### The Difference Between a Recursive Resolver and an Authoritative Server

**Recursive Resolver:** The Resolver is the coordinator responsible for returning the IP address. It is the one that manages the "trip" between the servers until the IP address is obtained.

**Authoritative Server:** The Authoritative Server is the manager of the specific Name Server (NS). It either holds the final IP address itself or provides a redirection to another server that holds its exact IP address.

### Troubleshooting Scenario: Is it a DNS Issue or a Web Server Issue?

**Scenario:** A user reports that a service/website is inaccessible. We need to investigate whether the issue is with name resolution (DNS) or the actual web server.

#### Step 1: Run a DNS lookup command (`nslookup` or `dig`)
We query the domain name to see if we can resolve it to an IP address.

#### SAnalyze the results
**Case A: No DNS response at all (Resolution Fails)**
  * *Result:* The command returns an error..
  * *Conclusion:* The issue is a **DNS failure**. The Recursive Resolver or the Authoritative NS server is down, meaning the system cannot translate the domain name into an IP address. The request never even reached the web server.

**Case B: DNS returns a valid IP, but the site still won't load**
  * *Result:* You successfully receive the target IP address, but the browser still shows a "Connection Timed Out" error.
  * *Conclusion:* The **DNS system is working perfectly**. The issue lies further down the line—the actual web server hosting the site has crashed, or there is a network/firewall issue blocking the traffic.

* **Case C: No IP is returned at the end of the chain**
  * *Result:* The Resolver manages the trip through the Root and TLD servers, but when it queries the final Authoritative Name Server (NS), it receives no response or an error, and no IP address is obtained.
  * *Conclusion:* The Authoritative NS server has crashed or is completely unavailable. The translation process broke at the final step.


