---
layout: post
title: "HITB CTF 2016: 'Special Delivery' writeup"
categories: writeups hitbctf
tags: network
author: saelo
---

Just a small writeup for "Special Delivery" (network 300) from HITB CTF 2016.

For this challenge we're provided with a [pcap](https://github.com/kitctf/writeups/raw/master/hitb2016/special_delivery/5d176b7cb326f05a1985be5d4d4d9074_special_delivery.pcap).

Looking at wireshark reveals two things:

1. The only packets inside the pcap are ICMP packets and IP fragments of ICMP packets
2. The ICMP packets contain interesting payload data

==> Things look a lot like an ICMP tunnel.

Let's get this solved with scapy. I solved the challenge mostly inside an interactive scapy shell so we'll do the same here:

    > scapy
    >>> pcap = rdpcap('5d176b7cb326f05a1985be5d4d4d9074_special_delivery.pcap')
    >>> pcap
    <5d176b7cb326f05a1985be5d4d4d9074_special_delivery.pcap: TCP:0 UDP:0 ICMP:267 Other:41>

Alright, let's get rid of the fragments:

    >>> pcap = defragment(pcap)
    >>> pcap
    <Defragmented 5d176b7cb326f05a1985be5d4d4d9074_special_delivery.pcap: TCP:0 UDP:0 ICMP:267 Other:0>

Good.

It seems not every packet has a payload though:

    >>> pcap[0]
    <Ether  dst=00:50:56:e8:3e:63 src=00:0c:29:c2:2c:40 type=0x800 |<IP  version=4L ihl=5L tos=0x0 len=28 id=22216 flags=DF frag=0L ttl=64 proto=icmp chksum=0x41b0 src=10.13.37.145 dst=192.168.178.34 options=[] |<ICMP  type=echo-request code=0 chksum=0x86e2 id=0x711d seq=0x0 |>>>
    >>> pcap[10]
    <Ether  dst=00:50:56:e8:3e:63 src=00:0c:29:c2:2c:40 type=0x800 |<IP  version=4L ihl=5L tos=0x0 len=88 id=22893 flags=DF frag=0L ttl=64 proto=icmp chksum=0x3ecf src=10.13.37.145 dst=192.168.178.34 options=[] |<ICMP  type=echo-request code=0 chksum=0xa113 id=0x711d seq=0x0 |<Raw  load='E\x00\x00<#\xe1@\x00@\x06\xfc\xd8\n\x00\x03\x02\n\x00\x03\x01\xba\xa1\x00P\xbb4\xd5\x89\x00\x00\x00\x00\xa0\x02r\x10y\x94\x00\x00\x02\x04\x05\xb4\x04\x02\x08\n\x00=\xf6h\x00\x00\x00\x00\x01\x03\x03\n' |>>>>

Let's remove the ones that don't have any content:

    >>> packets = [p for p in pcap if Raw in p]

Looking at the ICMP payloads, it looks like there's some binary stuff in every packet...
At this point I made a simple guess and assumed that the payload in the ICMP packets were IP packets themselves.
We can quickly verify this:

    >>> ip = IP(packets[0][Raw].load)
    >>> ip
    <IP  version=4L ihl=5L tos=0x0 len=60 id=9185 flags=DF frag=0L ttl=64 proto=tcp chksum=0xfcd8 src=10.0.3.2 dst=10.0.3.1 options=[] |<TCP  sport=47777 dport=http seq=3140801929 ack=0 dataofs=10L reserved=0L flags=S window=29200 chksum=0x7994 urgptr=0 options=[('MSS', 1460), ('SAckOK', ''), ('Timestamp', (4060776, 0)), ('NOP', None), ('WScale', 10)] |>>

Ok, this looks like a valid IP packet. Especially the dst and src look good.
Let's extract the actual IP packets:

    >>> packets = PacketList([IP(p[Raw].load) for p in packets])
    >>> packets
    <PacketList: TCP:175 UDP:0 ICMP:0 Other:0>

We could probably do the next steps with Wireshark, but let's write some more python while we're at it.

Quickly scanning the communication (e.g. `packets.summary()`), it looks like there are only two parties involved.
Let's split the packets by source IP (and filter out packets without content again):

    >>> client_packets = PacketList([p for p in packets if p[IP].src == '10.0.3.2' and Raw in p])
    >>> server_packets = PacketList([p for p in packets if p[IP].src == '10.0.3.1' and Raw in p])

Looking at the first few client packets (e.g. `client_packets[:10].hexdump()`) shows us that this is an HTTP GET request. Let's dump the response body to a file.

    >>> response = ''.join(packet[Raw].load for packet in server_packets)
    >>> header_length = response.find('\r\n\r\n') + 4
    >>> print(response[:header_length])
    HTTP/1.1 200 OK
    Date: Sun, 21 Feb 2016 16:51:19 GMT
    Server: Apache/2.2.22 (Debian)
    X-Powered-By: PHP/5.4.4-14+deb7u14
    Content-Description: File Transfer
    Content-Disposition: attachment; filename="stunnelshell.tgz"
    Content-Length: 59913
    Expires: 0
    Cache-Control: must-revalidate
    Pragma: public
    Keep-Alive: timeout=5, max=100
    Connection: Keep-Alive
    Content-Type: application/octet-stream

    >>> with open('response', 'w') as f:
    ...     f.write(response[header_length:])

[Different shell]
 
    > file response
    response: gzip compressed data, from Unix, last modified: Sun Feb 21 17:32:52 2016
    > tar -xfz response
    > ls
    response        stunnel         stunnel.pem     stunnel4        stunnelshell.sh

Ok, seems like the rest of the communication is encrypted using SSL through stunnel. Luckily we have the certificate (stunnel.pem).. and apparently no forward secrecy was used ;)

We'll now need Wireshark. For that we can either write a new pcap file containing the actual IP traffic:

    >>> wrpcap('special_delivery.pcap', packets)

Or, even simpler, start Wireshark directly from scapy:

    >>> wireshark(packets)

First we'll need to mark the encrypted packets as SSL traffic: `Rightclick -> Decode As -> SSL`.
There's a feature in wireshark for decrypting SSL traffic. It's somewhat hidden though: `Preferences -> Protocols -> SSL -> RSA keys list -> Key File`.
Now all that remains is to rightclick on one of the TLS packets and "Follow [the] SSL Stream":

    id
    uid=0(root) gid=0(root) groups=0(root)
    cd /root
    cat .flag
    HitB{b3a64ecf6978f0593ed20ee15a02ef36}
    exit

:)
