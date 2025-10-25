import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from openai import OpenAI
from openai.types import Video


# --------------------------------------------------------------
# Download helper (from official examples)
# --------------------------------------------------------------
def download_sora_video(
    video: Video,
    output_folder: str,
    filename: str = None,
    extension: str = ".mp4",
) -> Video:
    client = OpenAI()
    progress = getattr(video, "progress", 0)
    bar_length = 30

    if filename is None:
        filename = video.id

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = f"{output_folder}/{filename}{extension}"

    while video.status in ("in_progress", "queued"):
        video = client.videos.retrieve(video.id)
        progress = getattr(video, "progress", 0)
        filled_length = int((progress / 100) * bar_length)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        status_text = "Queued" if video.status == "queued" else "Processing"
        sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
        sys.stdout.flush()
        time.sleep(2)

    sys.stdout.write("\n")

    if video.status == "failed":
        message = getattr(getattr(video, "error", None), "message", "Video generation failed")
        print("❌", message)
        sys.exit(1)

    print("✅ Video generation completed:", video.id)
    print("⬇️  Downloading video content...")
    content = client.videos.download_content(video.id, variant="video")
    content.write_to_file(output_path)
    print(f"🎬 Saved video as {output_path}")
    return video


# --------------------------------------------------------------
# Image resize helper
# --------------------------------------------------------------
def resize_image_if_needed(path: Path, target_size: str):
    w, h = map(int, target_size.split("x"))
    img = Image.open(path)
    if img.size != (w, h):
        print(f"🖼️ Resizing {path.name} from {img.size} → {(w, h)}")
        img = img.resize((w, h))
        img.save(path)
    return path


# --------------------------------------------------------------
# Main script
# --------------------------------------------------------------
def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("❌ Missing OPENAI_API_KEY in .env")

    # --- Configuration ---
    model = "sora-2-pro"
    prompt = "Make a video of a real person that looks like the person in the image in a teams call. He should be looking into the camera for a few seconds and then start talking. He should wear clothes from the time of 247 before Christ."
    size = "720x1280"
    seconds = 8
    image_path = Path("input_images/photo.jpg")

    if not image_path.exists():
        raise FileNotFoundError(f"❌ File not found: {image_path}")

    image_path = resize_image_if_needed(image_path, size)

    print("🎞️  Submitting Sora generation request...")
    video = client.videos.create(
        model=model,
        prompt=prompt,
        input_reference=image_path,
        size=size,
        seconds=seconds,
    )

    print(f"🆔 Job created: {video.id} (status={video.status})")

    # --- Wait for completion + download ---
    download_sora_video(video, output_folder="./output")


if __name__ == "__main__":
    main()
