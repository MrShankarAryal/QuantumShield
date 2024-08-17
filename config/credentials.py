class Credentials:
    def __init__(self):
        self.API_KEY = "YOUR_API_KEY_HERE"
        self.SECRET_KEY = "YOUR_SECRET_KEY_HERE"

if __name__ == "__main__":
    credentials = Credentials()
    print(f"API Key: {credentials.API_KEY}")
