import unittest
from network_monitor.traffic_analyzer import TrafficAnalyzer
from network_monitor.honeypots import Honeypots
from unittest.mock import patch
from scapy.all import IP


class TestTrafficAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TrafficAnalyzer()
        self.analyzer.suspicious_ips.add("192.168.1.105")

    @patch('scapy.all.sniff')
    def test_packet_callback(self, mock_sniff):
        with patch('builtins.print') as mocked_print:
            mock_sniff.side_effect = lambda prn, store=0: prn(IP(src="192.168.1.105"))
            self.analyzer.monitor_traffic()
            mocked_print.assert_called_with("Suspicious activity detected from 192.168.1.105")

class TestHoneypots(unittest.TestCase):
    @patch('os.system')
    def test_deploy_honeypot(self, mock_system):
        honeypots = Honeypots()
        honeypots.deploy_honeypot()
        mock_system.assert_called_with("sudo docker run -d --name honeypot -p 80:80 honeypot_image")

    @patch('os.system')
    def test_monitor_honeypot(self, mock_system):
        honeypots = Honeypots()
        honeypots.monitor_honeypot()
        mock_system.assert_called_with("sudo docker logs -f honeypot")

if __name__ == "__main__":
    unittest.main()
