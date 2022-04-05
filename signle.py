#!/usr/bin/python3.9
# Copyright (c) 2021 MobileCoin Inc.
# Copyright (c) 2021 The Forest Team

from forest.core import Bot, Message, run_bot, Response
from forest.pdictng import aPersistDict

class ReplayBot(Bot):
    def __init__(self):
        self.messages = aPersistDict("messages")
        super().__init__()

    async def do_replay(self, _: Message) -> str:
        output_text = ""
        for val in await self.messages.keys():
            output_text += f"key: {val},\n    val: {await self.messages.get(val)}\n"
        return output_text

    async def do_delete(self, _: Message) -> str:
        keys = await self.messages.keys()
        tasks = []
        for key in keys:
            task = await self.messages.remove(key)
            tasks.append(task)
        print(tasks)
        return "deleted log"
    
    async def do_kobold(self, _: Message) -> str:
        return 'very good, yeah'

    async def handle_message(self, message: Message) -> Response:

        if cmd := self.match_command(message):
            # invoke the function and return the response
            return await getattr(self, "do_" + cmd)(message)
        if message.text == "TERMINATE":
            return "signal session reset"

        if len(message.full_text):
            if message.source.startswith('+'):
                source = message.source[1:]
            else:
                source = message.source
            timestamp = message.timestamp
            message_key = str(source)+str(timestamp)
            self.messages[message_key] = message.full_text



if __name__ == "__main__":
    run_bot(ReplayBot)