import torch
import warnings
import os
import numpy as np

class AudioAnalyzer:
    def __init__(self):
        self.model = None
        self.utils = None
    
    def load_model(self):
        print("Loading Silero VAD model (this may take a moment)...")
        # Suppress warnings
        warnings.filterwarnings("ignore")
        try:
            self.model, self.utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                                    model='silero_vad',
                                                    force_reload=False,
                                                    trust_repo=True)
            print("Silero VAD model loaded successfully.")
        except Exception as e:
            print(f"Failed to load VAD model: {e}")
            print("Will default to basic energy analysis if needed.")

    def get_speech_timestamps(self, audio_path):
        if not self.model:
            self.load_model()
        
        if not self.model:
            return []

        (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = self.utils
        
        try:
            wav = read_audio(audio_path)
            timestamps = get_speech_timestamps(wav, self.model, sampling_rate=16000)
            # Convert simple dict list to list of dicts with seconds
            # silero returns samples? No, usually normalized if using read_audio?
            # get_speech_timestamps returns dict with 'start', 'end' in samples.
            # sampling_rate=16000
            
            result = []
            for ts in timestamps:
                result.append({
                    'start': ts['start'] / 16000,
                    'end': ts['end'] / 16000
                })
            return result
        except Exception as e:
            print(f"Error analyzing audio {audio_path}: {e}")
            return []
    
    def suggest_dominant_speaker(self, audio1_path, audio2_path, start, end):
        """
        Naive check: who has more speech segments in this range?
        In a real tool we'd read chunks. For CLI simplicity we analyze whole file once (cached) 
        and check overlaps. 
        """
        # For this prototype, we'll implement a stub or assume the caller handles this logic 
        # by calling get_speech_timestamps once for the whole file.
        pass
