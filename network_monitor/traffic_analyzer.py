from scapy.all import sniff, IP

class TrafficAnalyzer:
    def __init__(self):
        self.suspicious_ips = set()

    def packet_callback(self, packet):
        if IP in packet:
            if packet[IP].src in self.suspicious_ips:
                print(f"Suspicious activity detected from {packet[IP].src}")

    def monitor_traffic(self):
        sniff(prn=self.packet_callback, store=0)

if __name__ == "__main__":
    analyzer = TrafficAnalyzer()
    analyzer.suspicious_ips.add("192.168.1.105")
    analyzer.monitor_traffic()
