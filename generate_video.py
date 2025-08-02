import os, sys
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
from gtts import gTTS
from pydub import AudioSegment
import google.generativeai as genai

# ==== CONFIG ====
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your key
CHUNK_DURATION = 10
OUTPUT_RESOLUTION = 480
CHARACTER_IMG = "/content/character.jpg"
BGM_FILE = "/content/bg_music.mp3"

topic = input("Enter your Hindi topic: ")

# ==== 1. Generate Script ====
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")
prompt = f"{topic} पर 150-200 शब्दों का एक छोटा, रोचक और कहानी जैसा स्क्रिप्ट लिखो, जो 30-40 सेकंड के टेस्ट वीडियो के लिए उपयुक्त हो।"
response = model.generate_content(prompt)
script_text = response.text
with open("/content/script.txt", "w", encoding="utf-8") as f:
    f.write(script_text)

# ==== 2. Generate Voice ====
tts = gTTS(script_text, lang="hi")
tts.save("/content/voice.mp3")

# ==== 3. Split into Chunks ====
audio = AudioSegment.from_mp3("/content/voice.mp3")
chunk_length_ms = CHUNK_DURATION * 1000
chunks = []
for i in range(0, len(audio), chunk_length_ms):
    chunk = audio[i:i+chunk_length_ms]
    chunk_file = f"/content/chunk_{len(chunks)}.mp3"
    chunk.export(chunk_file, format="mp3")
    chunks.append(chunk_file)

# ==== 4. Animate Each Chunk ====
final_clips = []
for chunk in chunks:
    os.system(f"python /content/SadTalker/inference.py --driven_audio {chunk} --source_image {CHARACTER_IMG} --result_dir /content/results --still --preprocess full > /dev/null 2>&1")
    latest_clip = sorted(os.listdir("/content/results"))[-1]
    clip = VideoFileClip(f"/content/results/{latest_clip}").resize(height=OUTPUT_RESOLUTION)
    clip = clip.set_audio(AudioFileClip(chunk))
    final_clips.append(clip)

# ==== 5. Merge Video ====
merged_video = concatenate_videoclips(final_clips)
merged_video.write_videofile("/content/merged.mp4", codec="libx264", fps=25)

# ==== 6. Add Music ====
narration = AudioFileClip("/content/merged.mp4")
music = AudioFileClip(BGM_FILE).volumex(0.2).fx(lambda c: c.set_duration(narration.duration))
final_audio = CompositeAudioClip([narration, music])
final_video = VideoFileClip("/content/merged.mp4").set_a
