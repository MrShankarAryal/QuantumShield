import os

class AutonomousDefense:
    def isolate_system(self, ip_address):
        print(f"Isolating system with IP: {ip_address}")
        os.system(f"iptables -A INPUT -s {ip_address} -j DROP")

    def block_ip(self, ip_address):
        print(f"Blocking IP: {ip_address}")
        os.system(f"iptables -A INPUT -s {ip_address} -j REJECT")

if __name__ == "__main__":
    defense = AutonomousDefense()
    defense.isolate_system("192.168.1.101")
    defense.block_ip("192.168.1.102")
