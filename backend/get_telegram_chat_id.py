#!/usr/bin/env python3
"""
Script to get Telegram Chat ID for your bot
Usage: python get_telegram_chat_id.py
"""
import asyncio
import os
import sys
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

async def get_chat_id():
    """Get chat ID by checking bot updates"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env")
        print("\nPlease add your bot token to backend/.env:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        sys.exit(1)
    
    print(f"✅ Bot token found: {token[:20]}...")
    print("\n" + "="*60)
    print("📱 Getting Chat IDs from bot updates...")
    print("="*60)
    
    try:
        bot = Bot(token=token)
        
        # Remove webhook if exists
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook removed (if existed)")
        
        # Get bot info
        me = await bot.get_me()
        print(f"\n🤖 Bot Info:")
        print(f"   Username: @{me.username}")
        print(f"   Name: {me.first_name}")
        print(f"   ID: {me.id}")
        
        # Get updates
        print("\n📬 Fetching recent messages...")
        updates = await bot.get_updates()
        
        if not updates:
            print("\n⚠️  No messages found!")
            print("\n📝 To get your Chat ID:")
            print("   1. Start a chat with your bot: @primary_production_d896a_bot")
            print("   2. Send any message to the bot")
            print("   3. Run this script again")
            return
        
        print(f"\n✅ Found {len(updates)} messages!\n")
        
        # Track unique chats
        chats_found = {}
        
        for update in updates:
            if update.message:
                chat = update.message.chat
                chat_id = chat.id
                chat_type = chat.type
                
                if chat_id not in chats_found:
                    chats_found[chat_id] = {
                        'type': chat_type,
                        'title': chat.title if chat.title else chat.first_name or 'Unknown',
                        'username': chat.username
                    }
        
        # Display results
        print("="*60)
        print("📋 CHAT IDs FOUND:")
        print("="*60)
        
        for chat_id, info in chats_found.items():
            print(f"\n🆔 Chat ID: {chat_id}")
            print(f"   Type: {info['type']}")
            print(f"   Name: {info['title']}")
            if info['username']:
                print(f"   Username: @{info['username']}")
            
            # Suggest which one to use
            if info['type'] == 'private':
                print("   💡 Use this for: Private messages to yourself")
            elif info['type'] == 'channel':
                print("   💡 Use this for: Public channel posts")
            elif info['type'] in ['group', 'supergroup']:
                print("   💡 Use this for: Group/channel posts")
        
        print("\n" + "="*60)
        print("📝 Add to your .env file:")
        print("="*60)
        
        # Suggest based on most recent or private chat
        for chat_id, info in chats_found.items():
            if info['type'] == 'private':
                print(f"\nTG_PUBLIC_CHAT_ID={chat_id}")
                print("# ↑ For private messages (testing)")
                break
            elif info['type'] in ['channel', 'supergroup']:
                print(f"\nTG_PUBLIC_CHAT_ID={chat_id}")
                print("# ↑ For channel/group posts (production)")
                break
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible issues:")
        print("1. Invalid bot token")
        print("2. Bot not started (@primary_production_d896a_bot)")
        print("3. No messages sent to bot yet")
        sys.exit(1)

if __name__ == "__main__":
    print("\n🤖 Telegram Chat ID Finder")
    print("="*60)
    asyncio.run(get_chat_id())


