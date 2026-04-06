import os
import discord
from discord.ext import commands
import datetime

# --- การตั้งค่า ---

# ใส่ ID ของห้องเสียงที่ต้องการเข้าไปสิงและเก็บ Log
CHANNEL_ID = 1433666298260230246

client = commands.Bot(command_prefix="!", self_bot=True)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # เชื่อมต่อห้องเสียง
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        # self_mute, self_deaf เพื่อความเนียนและประหยัดเน็ต
        await channel.connect(self_mute=True, self_deaf=True)
        print(f'Joined voice channel: {channel.name}')
        print('--- Waiting for users to join/leave ---')
    else:
        print("Channel not found")


@client.event
async def on_voice_state_update(member, before, after):
    # ป้องกันบอทเก็บ Log ตัวเอง
    if member.id == client.user.id:
        return

    # เวลาปัจจุบัน
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = ""

    # กรณี: มีคนเข้าห้อง (Joined)
    # เช็คว่า channel ใหม่คือห้องเป้าหมาย และ channel เก่าต้องไม่ใช่ห้องเป้าหมาย
    if after.channel and after.channel.id == CHANNEL_ID:
        if before.channel is None or before.channel.id != CHANNEL_ID:
            log_msg = f"[{now}] ✅ {member.name} (ID: {member.id}) เข้าห้องมาแล้ว"

    # กรณี: มีคนออกจากห้อง (Left)
    # เช็คว่า channel เก่าคือห้องเป้าหมาย และ channel ใหม่ไม่ใช่ห้องเป้าหมาย
    elif before.channel and before.channel.id == CHANNEL_ID:
        if after.channel is None or after.channel.id != CHANNEL_ID:
            log_msg = f"[{now}] ❌ {member.name} (ID: {member.id}) ออกจากห้องไปแล้ว"

    # ถ้ามีข้อความ Log ให้ปรินต์และบันทึกไฟล์
    if log_msg:
        print(log_msg)

        # บันทึกลงไฟล์ log.txt (ต่อท้ายไปเรื่อยๆ)
        with open("voice_history_log.txt", "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")


client.run(os.getenv('TOKEN'))
