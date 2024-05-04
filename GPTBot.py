# -*- coding:utf-8 -*-

"""
@author: 87-MyFriends
@version: 1.0.0
@date: 2024/4/14
@function:
"""
from openai import OpenAI


class GPTBot:
    def __init__(self):
        self.client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key="sk-88i5jsr2IKhWYqw5KjIiB3WpyJepn2mxyS3VYDzophKb9FhF",
            base_url="https://api.chatanywhere.tech/v1"
            # base_url="https://api.chatanywhere.cn/v1"
        )
        self.msgs = []

    # 非流式响应
    def gpt_35_api(self, messages):
        """为提供的对话消息创建新的回答

        Args:
            :param messages: 完整的对话消息列表，包含用户和机器人的消息
        """
        if len(self.msgs) > 3:
            del self.msgs[0]
        self.msgs.append(messages)
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=self.msgs)
        print(completion.choices[0].message.content)
        self.msgs.append({'role': 'assistant', 'content': completion.choices[0].message.content})

    def gpt_35_api_stream(self, messages):
        """为提供的对话消息创建新的回答 (流式传输)

        Args:
            :param messages: 完整的对话消息列表，包含用户和机器人的消息
        """
        if len(self.msgs) > 3:
            del self.msgs[0]
        self.msgs.append(messages)
        stream = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=self.msgs,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")


if __name__ == '__main__':
    bot = GPTBot()
    while True:
        content = input("User: ")
        # 非流式调用
        bot.gpt_35_api({"role": "user", "content": content})
        # 流式调用
        # gpt_35_api_stream(messages)
