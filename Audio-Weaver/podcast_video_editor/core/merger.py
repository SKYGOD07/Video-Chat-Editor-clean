import os
import shutil
from tqdm import tqdm
from .ffmpeg_engine import FFmpegEngine

class Merger:
    def __init__(self):
        self.engine = FFmpegEngine()
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def merge_segments(self, segments, video_path, audio1_path, audio2_path, final_output_name="final_podcast.mp4"):
        temp_files = []
        list_file_path = os.path.join(self.output_dir, "segments.txt")
        
        print(f"\nRendering {len(segments)} segments...")
        
        try:
            with open(list_file_path, "w") as f:
                for i, seg in enumerate(tqdm(segments)):
                    seg_filename = f"segment_{i:03d}.mp4"
                    seg_path = os.path.join(self.output_dir, seg_filename)
                    
                    self.engine.render_segment(
                        video_path, 
                        audio1_path, 
                        audio2_path, 
                        seg['start'], 
                        seg['end'], 
                        seg['priority'], 
                        seg_path
                    )
                    
                    temp_files.append(seg_filename)
                    f.write(f"file '{seg_filename}'\n")

            final_path = os.path.join(self.output_dir, final_output_name)
            print("Merging segments into final video...")
            self.engine.merge_videos(list_file_path, final_path)
            print(f"\nSuccess! Output saved to: {final_path}")
            
        finally:
            # Cleanup temp segment files
            print("Cleaning up temporary files...")
            for tf in temp_files:
                try:
                    os.remove(os.path.join(self.output_dir, tf))
                except:
                    pass
            if os.path.exists(list_file_path):
                os.remove(list_file_path)
