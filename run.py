from dotenv import load_dotenv

load_dotenv()

import app
bot = app.init()
app = bot.asgi
if __name__ == '__main__':
    bot.run(use_reloader=True)