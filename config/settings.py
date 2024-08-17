class Settings:
    def __init__(self):
        self.DEBUG = True
        self.THREAT_FEED_URL = "https://example.com/threat_feed"
        self.LOG_FILE = "./data/logs/quantumshield.log"

if __name__ == "__main__":
    settings = Settings()
    print(f"Debug Mode: {settings.DEBUG}")

