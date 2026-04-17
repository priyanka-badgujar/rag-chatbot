class Chatbot:
    def __init__(self):
        self.name = "StarterBot"

    def respond(self, message: str) -> str:
        if not message.strip():
            return "Please say something."
        return f"Echo: {message}"
