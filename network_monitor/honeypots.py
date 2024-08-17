import os

class Honeypots:
    def deploy_honeypot(self):
        os.system("sudo docker run -d --name honeypot -p 80:80 honeypot_image")

    def monitor_honeypot(self):
        os.system("sudo docker logs -f honeypot")

if __name__ == "__main__":
    honeypots = Honeypots()
    honeypots.deploy_honeypot()
    honeypots.monitor_honeypot()
