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

# Sidekickブラウザのパスを指定
browser = Browser(
    config=BrowserConfig(
        headless=False,  # ブラウザを表示する
        chrome_instance_path="/Applications/Sidekick.app/Contents/MacOS/Sidekick",  # Sidekickブラウザのパス
        disable_security=True,
        new_context_config=BrowserContextConfig(
            disable_security=True,
            minimum_wait_page_load_time=1,
            maximum_wait_page_load_time=10,
            browser_window_size={
                'width': 1280,
                'height': 1100,
            },
        ),
    )
)

llm = ChatOpenAI(model='gpt-4o')
agent = Agent(
    task='Go to x.com and tweet "Hello, world!"',
    llm=llm,
    browser=browser,
)

async def main():
    await agent.run(max_steps=10)
    agent.create_history_gif()

if __name__ == '__main__':
    asyncio.run(main()) 