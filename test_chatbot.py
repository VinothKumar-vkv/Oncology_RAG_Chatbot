from src.chatbot import OncologyChatbot

print("Loading chatbot...")
bot = OncologyChatbot()

print("Calling ask()...")
result = bot.ask("What is cancer?")

print("\n========== RESULT ==========")
print(result)
print("============================")
