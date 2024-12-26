import interpreter
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.agent.service import Agent
from langchain_openai import ChatOpenAI
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Open Interpreterの設定
interpreter.auto_run = True
interpreter.model = "gpt-4"

# Browser Useの設定
browser = Browser(
    config=BrowserConfig(
        headless=False,
        chrome_instance_path="/Applications/Sidekick.app/Contents/MacOS/Sidekick",
        disable_security=True,
    )
)

llm = ChatOpenAI(model='gpt-4')

async def tweet_with_image(text: str, image_path: str):
    # Browser Useのエージェントを設定
    agent = Agent(
        task=f'Go to x.com and tweet "{text}". Add the image from the file upload dialog, then click the POST button',
        llm=llm,
        browser=browser,
    )

    # Open Interpreterを使用してファイル選択ダイアログを処理
    interpreter.chat(f"""
    When the browser opens a file upload dialog, I need you to:
    1. Wait for the dialog to appear
    2. Select the file at path: {image_path}
    3. Confirm the file selection
    """)

    # Browser Useでツイートを実行
    await agent.run(max_steps=10)
    agent.create_history_gif()

async def main():
    tweet_text = "Hello from Browser Use and Open Interpreter! 🤖"
    image_path = os.path.expanduser("~/Downloads/cutecat.jpg")
    await tweet_with_image(tweet_text, image_path)

if __name__ == "__main__":
    asyncio.run(main()) 