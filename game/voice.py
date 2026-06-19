from gtts import gTTS
import asyncio
import io
import pygame

pygame.init()
async def speak(text: str) -> None:
    clean_text: str = " ".join(str(text).split()).strip()
    if not clean_text:
        return

    audio_buffer: io.BytesIO = io.BytesIO()
    tts: gTTS = gTTS(text=clean_text, lang='vi', slow=False)
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: tts.write_to_fp(audio_buffer))
    audio_buffer.seek(0)
    sound: pygame.mixer.Sound = pygame.mixer.Sound(audio_buffer)
    channel: pygame.mixer.Channel = sound.play()
    while channel.get_busy():
        await asyncio.sleep(0.05)

    audio_buffer.close()