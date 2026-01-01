import subprocess
import os

class FFmpegEngine:
    def get_video_duration(self, video_path):
        try:
            cmd = [
                'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', video_path
            ]
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
            return float(output)
        except subprocess.CalledProcessError as e:
            print(f"Error getting duration: {e.output.decode()}")
            return 0.0

    def extract_audio(self, input_path, output_path, sample_rate=16000):
        """Extracts audio to WAV for analysis (16kHz mono recommended for VAD)."""
        cmd = [
            'ffmpeg', '-y', '-i', input_path, 
            '-vn', '-acodec', 'pcm_s16le', '-ar', str(sample_rate), '-ac', '1', 
            output_path
        ]
        print(f"Extracting audio from {os.path.basename(input_path)}...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def render_segment(self, video_path, audio1_path, audio2_path, start, end, priority, output_path):
        """
        Renders a single segment.
        priority: 'audio1', 'audio2', 'mix'
        """
        duration = end - start
        
        # Basic command construction
        # In a real full podcast editor, we might switch video angles based on speaker.
        # Since we only have "Main Video File", we assume we just keep the video 
        # but mix the audio.
        # If 'priority' implies switching video source, we would need multiple video inputs.
        # The prompt asks for "Path to main video file", "Path to audio file 1", "Path to audio file 2".
        # It seems the video is single source, but audio is multi-source.
        # "Arrange video cuts based on active speaker audio" -> implies we might cut OUT parts?
        # Or maybe "Arrange video cuts" means if we had multiple cameras. 
        # Given single video input, "cuts" likely means "segments of the timeline".
        
        # Audio mapping:
        # If 'audio1' priority: Volume of audio1 1.0, audio2 0.2 (ducking)? Or just mute others?
        # Let's assume 'priority' means that source is the primary audio.
        
        cmd = ['ffmpeg', '-y', '-ss', str(start), '-t', str(duration), '-i', video_path]
        
        # Add audio inputs (we might need to offset them if they don't start at 0, 
        # but here we assume all files are synced starting at 0)
        cmd.extend(['-ss', str(start), '-t', str(duration), '-i', audio1_path])
        cmd.extend(['-ss', str(start), '-t', str(duration), '-i', audio2_path])
        
        # Complex filter for audio mixing
        # [1:a] and [2:a] are the audio inputs
        filter_complex = ""
        if priority == 'audio1':
            filter_complex = "[1:a]volume=1.0[a1];[2:a]volume=0.0[a2];[a1][a2]amix=inputs=2:duration=first[outa]"
        elif priority == 'audio2':
            filter_complex = "[1:a]volume=0.0[a1];[2:a]volume=1.0[a2];[a1][a2]amix=inputs=2:duration=first[outa]"
        else: # mix
            filter_complex = "[1:a]volume=1.0[a1];[2:a]volume=1.0[a2];[a1][a2]amix=inputs=2:duration=first[outa]"
            
        cmd.extend(['-filter_complex', filter_complex, '-map', '0:v', '-map', '[outa]', '-c:v', 'libx264', '-c:a', 'aac', output_path])
        
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def merge_videos(self, list_file_path, output_path):
        cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_file_path, '-c', 'copy', output_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
