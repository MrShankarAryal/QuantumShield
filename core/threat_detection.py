import requests
import json

class ThreatDetection:
    def __init__(self, threat_feed_url):
        self.threat_feed_url = threat_feed_url

    def get_threat_data(self):
        response = requests.get(self.threat_feed_url)
        if response.status_code == 200:
            return json.loads(response.text)
        return {}

    def analyze_threats(self, threat_data):
        suspicious_ips = []
        for threat in threat_data:
            if threat['severity'] > 7:  # Example threshold
                suspicious_ips.append(threat['ip'])
        return suspicious_ips

if __name__ == "__main__":
    threat_feed = "https://example.com/threat_feed"
    detection = ThreatDetection(threat_feed)
    data = detection.get_threat_data()
    suspicious_ips = detection.analyze_threats(data)
    print("Suspicious IPs:", suspicious_ips)
