import whisper
import os
import subprocess
import logging
from datetime import datetime

# Configure logging
LOG_FORMAT = "- %(levelname)s - %(message)s"
logging.basicConfig(
    filename=f"../logs/transcription_{datetime.now().strftime('%Y-%m-%d_%H:%M')}.log",
    level=logging.DEBUG,
    format=LOG_FORMAT
)

INPUT_DIR = "../data/input/"
OUTPUT_DIR = "../data/output/"

def list_video_files(input_dir):
    """
    Lists all video files in the input directory.

    Args:
        input_dir (str): Directory to search for video files.

    Returns:
        list: List of video file names.
    """
    try:
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

        video_files = [
            f for f in os.listdir(input_dir)
            if f.lower().endswith(('.mp4', '.mkv', '.avi'))
        ]
        if not video_files:
            raise FileNotFoundError(f"No video files found in {input_dir}.")
        return video_files
    except Exception as e:
        logging.error(f"Error listing video files: {e}")
        raise


def extract_audio(video_path, output_audio_path):
    """
    Extracts audio from a video file using FFmpeg.

    Args:
        video_path (str): Path to the video file.
        output_audio_path (str): Path to save the extracted audio file.
    """
    try:
        logging.info(f"Starting audio extraction from {video_path}")
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        command = [
            "ffmpeg",
            "-i", video_path,
            "-ar", "16000",
            "-ac", "1",
            output_audio_path,
            "-y"
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Audio extraction completed: {output_audio_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg failed: {e}")
        raise RuntimeError("Failed to extract audio using FFmpeg.") from e
    except Exception as e:
        logging.error(f"Unexpected error in audio extraction: {e}")
        raise


def transcribe_audio(audio_path, model_name="medium"):
    """
    Transcribes audio using Whisper.

    Args:
        audio_path (str): Path to the audio file.
        model_name (str): Whisper model name.

    Returns:
        str: Transcription text.
    """
    try:
        logging.info(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        logging.debug("Model loaded successfully.")
        result = model.transcribe(audio_path, language="en")
        logging.info("Transcription completed successfully.")
        return result["text"]
    except RuntimeError as e:
        logging.error(f"Whisper failed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during transcription: {e}")
        raise


def transcribe_video(video_path, output_text_path, model_name="medium"):
    """
    Transcribes the audio from a video file using Whisper.

    Args:
        video_path (str): Path to the video file.
        output_text_path (str): Path to save the transcription text.
        model_name (str): Whisper model name.

    Returns:
        None
    """
    audio_path = "temp_audio.wav"  # Temporary file for extracted audio
    try:
        logging.info(f"Processing video file: {video_path}")
        extract_audio(video_path, audio_path)
        transcription = transcribe_audio(audio_path, model_name)

        # Save transcription to the specified file
        os.makedirs(os.path.dirname(output_text_path), exist_ok=True)
        with open(output_text_path, "w") as f:
            f.write(transcription)
        logging.info(f"Transcription saved to {output_text_path}")
    except Exception as e:
        logging.error(f"Failed to transcribe video {video_path}: {e}")
        raise
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logging.info(f"Temporary audio file removed: {audio_path}")


if __name__ == "__main__":
    try:
        # List available files in INPUT_DIR
        video_files = list_video_files(INPUT_DIR)
        print("Available video files:")
        for idx, file_name in enumerate(video_files, 1):
            print(f"{idx}: {file_name}")

        # Prompt user to select a file
        file_index = int(input("Enter the number of the file to transcribe: ").strip()) - 1
        if file_index < 0 or file_index >= len(video_files):
            raise IndexError("Invalid file number selected.")

        # Set input and output paths
        selected_file = video_files[file_index]
        video_file_path = os.path.join(INPUT_DIR, selected_file)
        output_file_name = os.path.splitext(selected_file)[0] + ".txt"
        output_file_path = os.path.join(OUTPUT_DIR, output_file_name)

        # Transcribe the video
        logging.info(f"Script started for file: {video_file_path}")
        transcribe_video(video_file_path, output_file_path, model_name="medium.en")
        print(f"Transcription completed and saved to {output_file_path}.")
    except Exception as e:
        logging.critical(f"Script terminated due to error: {e}")
        print(f"Error: {e}")
    finally:
        logging.info("Script execution completed.")
