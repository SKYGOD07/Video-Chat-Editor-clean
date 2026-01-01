import os
import sys
from core.input_handler import InputHandler
from core.ffmpeg_engine import FFmpegEngine
from core.audio_analyzer import AudioAnalyzer
from core.timeline_manager import TimelineManager
from core.merger import Merger
from utils.time_parser import seconds_to_hms

def main():
    print("==========================================")
    print("   TERMINAL PODCAST VIDEO EDITOR v1.0")
    print("==========================================")
    
    input_handler = InputHandler()
    ffmpeg = FFmpegEngine()
    
    # 1. Get Inputs
    print("\n--- Input Files ---")
    video_path = input_handler.get_file_path("Path to Main Video: ", extensions=['.mp4', '.mov', '.mkv'])
    audio1_path = input_handler.get_file_path("Path to Speaker A Audio: ", extensions=['.wav', '.mp3', '.m4a'])
    audio2_path = input_handler.get_file_path("Path to Speaker B Audio: ", extensions=['.wav', '.mp3', '.m4a'])
    
    # 2. Analyze
    print("\n--- Analysis ---")
    duration = ffmpeg.get_video_duration(video_path)
    print(f"Video Duration: {seconds_to_hms(duration)}")
    
    # Convert audio to 16khz wav for VAD
    temp_audio1 = "temp_audio1.wav"
    temp_audio2 = "temp_audio2.wav"
    ffmpeg.extract_audio(audio1_path, temp_audio1)
    ffmpeg.extract_audio(audio2_path, temp_audio2)
    
    analyzer = AudioAnalyzer()
    # In a full run, we would analyze here. For now we load model to ensure it works.
    analyzer.load_model()
    
    # 3. Interactive Editing
    timeline = TimelineManager()
    
    print("\n--- Timeline Editor ---")
    num_segments = input_handler.get_int("How many timeline segments do you want to create? ", min_val=1)
    
    for i in range(num_segments):
        print(f"\nSegment {i+1}/{num_segments}")
        start = input_handler.get_time("Start time (HH:MM:SS): ")
        end = input_handler.get_time("End time (HH:MM:SS): ")
        
        if end > duration:
            print(f"Warning: End time exceeds video duration ({seconds_to_hms(duration)}). Clamping to duration.")
            end = duration
            
        priority = input_handler.get_choice("Prioritize audio source (audio1 / audio2 / mix): ", ['audio1', 'audio2', 'mix'])
        
        if timeline.add_segment(start, end, priority):
            print("Segment added.")
    
    # 4. Silence Removal Option
    remove_silence = input_handler.get_yes_no("\nRun silence removal (experimental)?")
    if remove_silence:
        print("Silence removal is enabled (simulation mode for this version).")
        # In full version, we'd modify timeline segments here
    
    # 5. Export
    merge_files = input_handler.get_yes_no("\nMerge all segments into one final video?")
    
    if merge_files:
        merger = Merger()
        merger.merge_segments(timeline.get_segments(), video_path, audio1_path, audio2_path)
    else:
        print("Skipping merge. Segments defined but not rendered.")
    
    # Cleanup
    if os.path.exists(temp_audio1): os.remove(temp_audio1)
    if os.path.exists(temp_audio2): os.remove(temp_audio2)
    
    print("\nDone. Exiting.")

if __name__ == "__main__":
    main()
