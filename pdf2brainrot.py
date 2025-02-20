import os
import fitz
import argparse
import torch
import numpy as np
from scipy.io import wavfile
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_audioclips, AudioArrayClip
from kokoro import KPipeline

# Input and Output Files
BASE_VIDEO = "videoplayback.mp4"
SCRIPT_PATH = "kokoro_script.txt"
OUTPUT_VIDEO = "final_video.mp4"
FONT_PATH = "./Roboto-ExtraBold.ttf"  # Ensure this font file exists
TEXT_LEAD_TIME = 0.5  # How many seconds the text appears before the audio
PAUSE_DURATION = 0.2  # Silence duration in seconds when encountering \n
AUDIO_SAMPLE_RATE = 24000  # 24kHz sample rate

# Function to generate a silent audio clip
def generate_silence(duration, sample_rate=AUDIO_SAMPLE_RATE):
    """Generates a silent audio clip of the given duration."""
    num_samples = int(duration * sample_rate)
    silence_array = np.zeros((num_samples, 1), dtype=np.float32)  # Ensure 2D array
    return AudioArrayClip(silence_array, fps=sample_rate)


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file and saves it into a text file.
    
    :param pdf_path: Path to the input PDF file.
    """
    output_text_file = SCRIPT_PATH
    with fitz.open(pdf_path) as doc:
        text = "\n".join([page.get_text("text") for page in doc])

    with open(output_text_file, "w", encoding="utf-8") as text_file:
        text_file.write(text)
    
    print(f"✅ Text extracted and saved to: {output_text_file}")

# Function to generate TTS audio and stitch it together
def generate_tts_audio(text, voice="af_heart", speed=1):
    pipeline = KPipeline(lang_code='a')  # English
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=r'\n+')

    audio_clips = []
    
    for gs, ps, audio in generator:
        audio = audio.to(device)
        audio_np = audio.cpu().numpy()
        audio_int16 = (audio_np * 32767).astype("int16")

        # Save each generated segment to a temporary WAV file
        temp_audio_path = f"temp_{len(audio_clips)}.wav"
        wavfile.write(temp_audio_path, AUDIO_SAMPLE_RATE, audio_int16)
        audio_clips.append(AudioFileClip(temp_audio_path))

        # Add a small pause after each segment
        pause_clip = generate_silence(PAUSE_DURATION)
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

# Function to overlay generated audio on video and trim video length
def overlay_audio_on_video(video_path, audio_path, output_path=OUTPUT_VIDEO):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Trim video to the length of the generated audio
    video = video.subclipped(0, audio.duration)

    # Set the new audio on the video
    video = video.with_audio(audio)

    video.write_videofile(output_path, codec="libx264", fps=video.fps)
    print(f"✅ Final video saved as {output_path}")

# Function to generate and overlay text with lead time
def overlay_text_on_video(video_path, script_text, output_path="final_video_with_subs.mp4"):
    video = VideoFileClip(video_path)

    words = script_text.split()
    duration = video.duration
    word_duration = duration / len(words)

    text_clips = []
    for i, word in enumerate(words):
        start_time = max(0, (i * word_duration) - TEXT_LEAD_TIME)  # Shift text earlier
        end_time = start_time + word_duration

        txt_clip = (TextClip(
                        text=word, 
                        font_size=70,  # Bigger text
                        font=FONT_PATH, 
                        color='white', 
                        stroke_color='black',  # Outline for thickness
                        stroke_width=7  # Make the text thicker
                    )
                    .with_position("center")  # Centered text
                    .with_duration(word_duration)
                    .with_start(start_time))

        text_clips.append(txt_clip)

    final_video = CompositeVideoClip([video] + text_clips)
    final_video.write_videofile(output_path, codec="libx264", fps=video.fps)
    print(f"✅ Final video with subtitles saved as {output_path}")

# Main function to run the pipeline
def main():
    # Read script and generate TTS audio
    with open(SCRIPT_PATH, "r", encoding="utf-8") as file:
        script_text = file.read()

    tts_audio_file = generate_tts_audio(script_text)

    # Overlay TTS audio on video and trim to audio length
    overlay_audio_on_video(BASE_VIDEO, tts_audio_file)

    # Add centered bold subtitles with text leading audio
    overlay_text_on_video(OUTPUT_VIDEO, script_text)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Extract text from a PDF and save it to a text file.")
    # parser.add_argument("--source", "-s", required=True, help="Path to the source PDF file.")

    # args = parser.parse_args()

    # extract_text_from_pdf(args.source)
    main()
