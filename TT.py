from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import GiftEvent, JoinEvent
import processor

processor.start()

print("....")
# Tiktok username to get data from
client: TikTokLiveClient = TikTokLiveClient(unique_id="@")
print("started")

@client.on("gift")
async def on_gift(event: GiftEvent):
    # If it's type 1 and the streak is over
    if event.gift.info.type == 1:
        if event.gift.repeat_end == 1:
            text = f"{event.user.unique_id}  {event.gift.count} ədəd \"{event.gift.info.name}\" göndərdi."
            print(text)
            processor.add(text)

    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.info.type != 1:
        text = f"{event.user.unique_id} \"{event.gift.info.name}\" göndərdi."
        print(text)
        processor.add(text)
        
@client.on("join")
async def on_join(event: JoinEvent):
    text = f"@{event.user.unique_id} canl\u0131ya qoşuldu."
    print(text)
    processor.add(text)

if __name__ == '__main__':
    client.run()
    
    # Gift(id=5655, count=1, repeat_end=None, info=GiftInfo(image=TikTokImage(urls=['https://p16-webcast.tiktokcdn.com/img/maliva/webcast-va/eba3a9bb85c33e017f3648eaf88d7189~tplv-obj.png', 'https://p19-webcast.tiktokcdn.com/img/maliva/webcast-va/eba3a9bb85c33e017f3648eaf88d7189~tplv-obj.png'], uri='webcast-va/eba3a9bb85c33e017f3648eaf88d7189'), description='Sent Rose', type=1, diamond_count=1, name='Rose'), recipient=GiftRecipient(timestamp=1704744731751, user_id=7317977049753781281), detailed=None)