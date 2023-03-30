import os
from dotenv import load_dotenv


load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print(key)
os.system("sgpt --help")

os.environ["OPENAI_API_KEY"] = "qqqq"


print(os.environ["OPENAI_API_KEY"])
