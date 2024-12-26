"""
Example of using Sidekick browser with browser-use
"""

import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig

# タスクのリスト
TASKS = {
    "tweet": "Go to x.com and tweet 'Hello, world from cute AI agent'. add media to the tweet from Downlods/cutecat.jpg once you type the tweet and add media, click the POST button",
    "amazon_search": "Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result",
    "google_search": "Google検索で「最新のAI技術トレンド 2024」について検索し、最初の3つの結果の要約を教えてください。"
}

# Sidekickブラウザのパスを指定
browser = Browser(
    config=BrowserConfig(
        headless=False,  # ブラウザを表示する
        chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # Chromeブラウザのパス
        disable_security=True,
        new_context_config=BrowserContextConfig(
            disable_security=True,
            # minimum_wait_page_load_time=1,
            # maximum_wait_page_load_time=10,
            browser_window_size={
                'width': 1280,
                'height': 1100,
            },
        ),
    )
)

llm = ChatOpenAI(model='gpt-4o')

# タスクを選択（デフォルトはツイート）
selected_task = TASKS["tweet"]  # ここを変更することで異なるタスクを実行可能

agent = Agent(
    task=selected_task,
    llm=llm,
    browser=browser,
)

async def main():
    await agent.run(max_steps=10)
    agent.create_history_gif()

if __name__ == '__main__':
    asyncio.run(main())