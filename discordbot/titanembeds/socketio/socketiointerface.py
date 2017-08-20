import socketio
from titanembeds.utils import get_message_author, get_message_mentions

class SocketIOInterface:
    def __init__(self, bot, redis_uri):
        self.io = socketio.AsyncRedisManager(redis_uri, write_only=True, channel='flask-socketio')
        self.bot = bot
    
    async def on_message(self, message):
        if message.server:
            edit_ts = message.edited_timestamp
            if not edit_ts:
                edit_ts = None
            else:
                edit_ts = str(edit_ts)
            msg = {
                "id": message.id,
                "channel_id": message.channel.id,
                "content": message.content,
                "author": get_message_author(message),
                "timestamp": str(message.timestamp),
                "edited_timestamp": edit_ts,
                "mentions": get_message_mentions(message.mentions),
                "attachments": message.attachments,
            }
            await self.io.emit('MESSAGE_CREATE', data=msg, room=message.server.id, namespace='/gateway')