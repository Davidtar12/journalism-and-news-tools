import subprocess
import os
import sys
from typing import Tuple, Optional
import shutil
import tempfile

class VideoConverter:
    MAX_SIZE = 150 * 1024  # 150KB strict limit

    def __init__(self):
        self.temp_dir = None

    def __enter__(self):
        # Store the original working directory and switch to a temporary directory for FFmpeg pass logs
        self.original_dir = os.getcwd()
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Return to the original working directory and clean up temporary files
        os.chdir(self.original_dir)
        if self.temp_dir:
            shutil.rmtree(self.temp_dir)

    @staticmethod
    def check_dependencies() -> bool:
        """Verify FFmpeg and FFprobe are installed with proper codecs."""
        try:
            ffmpeg = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                check=True
            )
            if "libx264" not in ffmpeg.stdout:
                print("Warning: libx264 codec not found in FFmpeg")
                return False

            subprocess.run(
                ["ffprobe", "-version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Dependency check failed: {str(e)}")
            return False

    def get_video_info(self, input_file: str) -> Tuple[float, Tuple[int, int]]:
        """Get video duration and dimensions."""
        try:
            duration_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                input_file
            ]
            duration = float(subprocess.run(
                duration_cmd,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip())

            dim_cmd = [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height",
                "-of", "csv=s=x:p=0",
                input_file
            ]
            width, height = map(int, subprocess.run(
                dim_cmd,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip().split('x'))

            return duration, (width, height)
        except (subprocess.CalledProcessError, ValueError) as e:
            print(f"Error getting video info: {str(e)}")
            sys.exit(1)

    def convert_to_mp4(self, input_gif: str, output_mp4: str) -> Optional[str]:
        """Convert GIF to MP4 using two-pass encoding with strict size control."""
        if not os.path.exists(input_gif):
            print(f"Input file not found: {input_gif}")
            return None

        duration, _ = self.get_video_info(input_gif)
        target_bitrate = int((self.MAX_SIZE * 8) / duration * 0.95)

        for attempt in range(8):
            print(f"MP4 attempt {attempt + 1}: Bitrate {target_bitrate} bps")
            try:
                # First pass
                subprocess.run([
                    "ffmpeg", "-y", "-i", input_gif,
                    "-c:v", "libx264", "-b:v", f"{target_bitrate}",
                    "-preset", "slow", "-tune", "animation",
                    "-pass", "1", "-an", "-f", "null",
                    "-movflags", "+faststart",
                    "/dev/null"
                ], check=True, capture_output=True)

                # Second pass
                subprocess.run([
                    "ffmpeg", "-y", "-i", input_gif,
                    "-c:v", "libx264", "-b:v", f"{target_bitrate}",
                    "-preset", "slow", "-tune", "animation",
                    "-pass", "2", "-an",
                    "-movflags", "+faststart",
                    output_mp4
                ], check=True, capture_output=True)

                if os.path.exists(output_mp4):
                    size = os.path.getsize(output_mp4)
                    if size <= self.MAX_SIZE:
                        print(f"MP4 success: {size / 1024:.1f}KB")
                        return output_mp4
                    else:
                        os.remove(output_mp4)
                target_bitrate = int(target_bitrate * 0.85)

            except subprocess.CalledProcessError as e:
                print(f"MP4 encoding failed: {str(e)}")
                target_bitrate = int(target_bitrate * 0.85)
                if os.path.exists(output_mp4):
                    os.remove(output_mp4)

        print("Failed to create MP4 within size limit")
        return None

    def convert_to_webp(self, input_gif: str, output_webp: str) -> Optional[str]:
        """Convert GIF to WebP using binary search for optimal quality, with looping enabled."""
        if not os.path.exists(input_gif):
            print(f"Input file not found: {input_gif}")
            return None

        # Try lossless conversion first with maximum compression and loop enabled
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", input_gif,
                "-lossless", "1",
                "-compression_level", "6",
                "-quality", "100",
                "-loop", "0",  # Loop flag: infinite looping
                output_webp
            ], capture_output=True, check=True)

            if os.path.exists(output_webp) and os.path.getsize(output_webp) <= self.MAX_SIZE:
                print(f"WebP lossless success: {os.path.getsize(output_webp) / 1024:.1f}KB")
                return output_webp

            if os.path.exists(output_webp):
                os.remove(output_webp)
        except subprocess.CalledProcessError:
            pass

        # Binary search for optimal lossy quality with loop enabled
        low, high = 1, 100
        best_quality = None

        while low <= high:
            quality = (low + high) // 2
            try:
                subprocess.run([
                    "ffmpeg", "-y", "-i", input_gif,
                    "-compression_level", "6",
                    "-quality", str(quality),
                    "-loop", "0",  # Loop flag for infinite looping
                    output_webp
                ], capture_output=True, check=True)

                if os.path.exists(output_webp):
                    size = os.path.getsize(output_webp)
                    if size <= self.MAX_SIZE:
                        best_quality = quality
                        low = quality + 1
                    else:
                        high = quality - 1
                    os.remove(output_webp)
            except subprocess.CalledProcessError:
                high = quality - 1

        if best_quality is not None:
            try:
                subprocess.run([
                    "ffmpeg", "-y", "-i", input_gif,
                    "-compression_level", "6",
                    "-quality", str(best_quality),
                    "-loop", "0",  # Loop flag for infinite looping
                    output_webp
                ], capture_output=True, check=True)

                if os.path.exists(output_webp) and os.path.getsize(output_webp) <= self.MAX_SIZE:
                    print(f"WebP lossy success: {os.path.getsize(output_webp) / 1024:.1f}KB (quality: {best_quality})")
                    return output_webp
            except subprocess.CalledProcessError:
                pass

        print("Failed to create WebP within size limit")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input.gif>")
        sys.exit(1)

    input_gif = sys.argv[1]
    if not os.path.exists(input_gif):
        print(f"Input file not found: {input_gif}")
        sys.exit(1)

    if not input_gif.lower().endswith('.gif'):
        print("Input file must be a GIF")
        sys.exit(1)

    # Define the destination folder as "news gif folder" inside "C:\Users\david\Downloads"
    destination_dir = os.path.join("C:\\Users\\david\\Downloads", "news gif folder")
    os.makedirs(destination_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_gif))[0]
    output_mp4 = os.path.join(destination_dir, f"{base_name}.mp4")
    output_webp = os.path.join(destination_dir, f"{base_name}.webp")

    if not VideoConverter.check_dependencies():
        print("Required dependencies not found")
        sys.exit(1)

    with VideoConverter() as converter:
        print(f"\nProcessing: {input_gif}")
        print(f"Original size: {os.path.getsize(input_gif) / 1024:.1f}KB")

        mp4_path = converter.convert_to_mp4(input_gif, output_mp4)
        webp_path = converter.convert_to_webp(input_gif, output_webp)

        print("\nResults:")
        print(f"MP4: {'Success' if mp4_path else 'Failed'}")
        print(f"WebP: {'Success' if webp_path else 'Failed'}")

if __name__ == "__main__":
    main()
