# chat/firebase_utils.py
import firebase_admin
from firebase_admin import credentials, db
import datetime


def store_chat_message(sender_id, recipient_id, message):
    ref = db.reference(f'chats/{sender_id}_{recipient_id}')
    ref.push({
        'sender_id': sender_id,
        'recipient_id': recipient_id,
        'message': message,
        'timestamp': firebase_admin.db.ServerValue.TIMESTAMP
    })

def get_chat_messages(sender_id, recipient_id):
    ref = db.reference(f'chats/{sender_id}_{recipient_id}')
    messages = ref.get()
    if messages:
        return messages
    else:
        return []

# Example function to fetch messages and convert timestamps to datetime objects
def fetch_messages_with_timestamp_conversion(sender_id, recipient_id):
    messages = get_chat_messages(sender_id, recipient_id)
    converted_messages = []
    for key, message in messages.items():
        converted_message = {
            'sender_id': message['sender_id'],
            'recipient_id': message['recipient_id'],
            'message': message['message'],
            'timestamp': datetime.datetime.fromtimestamp(message['timestamp'] / 1000.0)
        }
        converted_messages.append(converted_message)
    return converted_messages
