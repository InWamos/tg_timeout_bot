from pyrogram import Client
import asyncio
import json

class Bot:

    def __init__(self) -> None:
        # Reads files
        with open('config/config.json', 'r') as config_json:
            self.data_json = json.loads(config_json.read())

        with open('config/text.txt', 'r') as config_txt:
            self.data_txt = config_txt.read()

    # Function to list all chats in session(A panel to choose  groups and supergroups among all chats)
    async def get_chats(self):
        self.chats_obj = {}
        self.counter = 1

        if len(self.data_json["chats_to_spam"]) > 0:
            print(f'Previous id\'s: {self.data_json["chats_to_spam"]}\n')
            self.start_function = input("Configure new id's? [y/n]: ")
            if self.start_function != 'y':
                return


        async with Client("bot", self.data_json["api_id"], self.data_json["api_hash"]) as app:

            async for dialog in app.get_dialogs():

                try:
                    if str(dialog.chat.type) == "ChatType.SUPERGROUP" or str(dialog.chat.type) == "ChatType.GROUP":
                        self.chats_obj[str(self.counter)] = {}
                        self.chats_obj[str(self.counter)]["id"] = dialog.chat.id
                        self.chats_obj[str(self.counter)]["chat_type"] = dialog.chat.type
                        
                        print(f'|\n| - [{self.counter}] {dialog.chat.title} ({dialog.chat.id})\n|')
                        self.counter += 1
                except:
                    raise Exception

            self.target_chat_number_raw_input = input("Enter the targets' numbers: ")
            self.targets_numbers = self.target_chat_number_raw_input.split(',')
            self.data_json["chats_to_spam"] = []


            for i in self.targets_numbers:

                if i in self.chats_obj:

                    self.data_json["chats_to_spam"].append(self.chats_obj[i]["id"])
            
            with open('config/config.json', 'w', encoding='utf-8') as config_file:
                config_file.write(json.dumps(self.data_json, ensure_ascii=False, indent=4))

            print("Launch the main.py now")

def main():

    bot = Bot()
    asyncio.run(bot.get_chats())

if __name__ == "__main__":
 
    main()    


 