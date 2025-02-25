import os
import argparse
from typing import List, Dict
import torch
import numpy as np
from scipy.io import wavfile
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_audioclips, AudioArrayClip
import whisper_timestamped as whisper
from kokoro import KPipeline

# Paths
BASE_VIDEO = "videoplayback.mp4"
SCRIPT_PATH = "kokoro_script.txt"
OUTPUT_VIDEO = "final_video.mp4"
FONT_PATH = "./Roboto-ExtraBold.ttf"
TTS_AUDIO_PATH = "tts_output.wav"

# Constants
PAUSE_DURATION = 0.2  # Silence duration in seconds when encountering \n
TEXT_LEAD_TIME = 0.3  # Small offset to display text before spoken
AUDIO_SAMPLE_RATE = 24000  # 24kHz

# GPU acceleration if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Function to generate a silent audio clip
def generate_silence(duration: float, sample_rate: int = AUDIO_SAMPLE_RATE) -> AudioArrayClip:
    """Generates a silent audio clip of the given duration."""
    num_samples = int(duration * sample_rate)
    silence_array = np.zeros((num_samples, 1), dtype=np.float32)  # Ensure 2D array
    return AudioArrayClip(silence_array, fps=sample_rate)

# Function to generate TTS audio and stitch it together
def generate_tts_audio(text: str, voice: str = "af_heart", speed: int = 1, lang_code: str = 'a') -> str:
    """Generates TTS audio using kokoro and stitches it together."""
    pipeline = KPipeline(lang_code=lang_code)  # English
    
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=r'\n+')

    audio_clips = []
    
    for gs, ps, audio in generator:
        audio = audio.to(device)
        audio_np = audio.cpu().numpy()
        audio_int16 = (audio_np * 32767).astype("int16")

        # Initial silence before each segment
        pause_clip = generate_silence(PAUSE_DURATION)
        audio_clips.append(pause_clip)

        # Save each generated segment to a temporary WAV file
        temp_audio_path = f"temp_{len(audio_clips)}.wav"
        wavfile.write(temp_audio_path, AUDIO_SAMPLE_RATE, audio_int16)
        audio_clips.append(AudioFileClip(temp_audio_path))

        # Add a small pause after each segment
        audio_clips.append(pause_clip)

    # Remove last pause to avoid extra silence at the end
    if audio_clips:
        audio_clips.pop()

    # Concatenate all audio segments
    final_audio = concatenate_audioclips(audio_clips)
    final_audio_path = "tts_output.wav"
    final_audio.write_audiofile(final_audio_path, fps=AUDIO_SAMPLE_RATE)

    # Cleanup temporary audio files
    for clip in audio_clips:
        if hasattr(clip, "filename") and os.path.exists(clip.filename):
            os.remove(clip.filename)

    print(f"✅ Stitched audio saved as {final_audio_path}")
    return final_audio_path  # Return the final audio file path


def extract_timestamps(audio_path: str) -> List[Dict[str, str | float]]:
    """Extract timestamps using Vosk but without using Whisper."""
    audio = whisper.load_audio(audio_path)

    model = whisper.load_model("small", device=device)

    result = whisper.transcribe(model, audio, language="en")

    word_timestamps = []
    for items in result["segments"]:
        for item in items["words"]:
            word_timestamps.append({"text": item["text"], "start": item["start"], "duration": round(float(item["end"]) - float(item["start"]), 5)})

    print(f"✅ Extracted {len(word_timestamps)} timestamps")
    return word_timestamps


def overlay_audio_on_video(video_path: str, audio_path: str, output_path: str) -> None:
    """Overlay TTS audio onto video."""
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    video = video.subclipped(0, audio.duration).with_audio(audio)
    video.write_videofile(output_path, codec="libx264", fps=video.fps)

    print(f"✅ Final video saved as {output_path}")


def overlay_text_on_video(video_path: str, aligned_words, output_path: str) -> None:
    """Overlay synchronized subtitles."""
    video = VideoFileClip(video_path)
    text_clips = []

    for i, word_data in enumerate(aligned_words):
        word, start_time, duration = word_data["text"], word_data["start"], word_data["duration"]
        start_time = max(0, start_time)

        txt_clip = (TextClip(
                        text=word,
                        font_size=70,
                        font=FONT_PATH,
                        color='white',
                        stroke_color='black',
                        stroke_width=7,
                        size=(720, 100)
                    )
                    .with_position("center")
                    .with_duration(duration)
                    .with_start(start_time))

        text_clips.append(txt_clip)

    final_video = CompositeVideoClip([video] + text_clips)
    final_video.write_videofile(output_path, codec="libx264", fps=video.fps)

    print(f"✅ Final video with subtitles saved as {output_path}")


def main() -> None:
    """Main function to generate brainrot with subtitles."""
    # Read script text
    with open(SCRIPT_PATH, "r", encoding="utf-8") as file:
        script_text = file.read().strip()

    # Generate TTS audio
    print("🔊 Generating TTS audio...")
    tts_audio_file = generate_tts_audio(script_text)

    # Overlay audio onto video
    print("🎞️ Overlaying audio onto video...")
    overlay_audio_on_video(BASE_VIDEO, tts_audio_file, OUTPUT_VIDEO)

    # Extract raw timestamps
    print("🕒 Extracting timestamps...")
    word_timestamps = extract_timestamps(tts_audio_file)

    # Overlay synchronized subtitles
    print("📝 Overlaying synchronized subtitles...")
    overlay_text_on_video(OUTPUT_VIDEO, word_timestamps, "final_video_with_subs.mp4")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a PDF file, summarize it, and generate brainrot with subtitles.")
    # parser.add_argument("--source", "-s", required=True, help="Path to the source PDF file.")
 
    args = parser.parse_args()

    # extract_text_from_pdf(args.source)
    main()
