from pydub import AudioSegment
import os
from models import StoreType

class AudioProcessor:
    STORE_SPECS = {
        StoreType.MTN: {
            "format": "mp3",
            "bitrate": "128k",
            "sample_rate": 44100,
            "max_duration": 30000,
            "channels": 2
        },
        StoreType.VODACOM: {
            "format": "aac",
            "bitrate": "96k",
            "sample_rate": 44100,
            "max_duration": 45000,
            "channels": 2
        },
        StoreType.TELKOM: {
            "format": "mp3",
            "bitrate": "192k",
            "sample_rate": 48000,
            "max_duration": 60000,
            "channels": 2
        }
    }
    
    @staticmethod
    def process_audio(input_path: str, output_path: str, store: StoreType) -> dict:
        specs = AudioProcessor.STORE_SPECS[store]
        audio = AudioSegment.from_file(input_path)
        
        if len(audio) > specs["max_duration"]:
            audio = audio[:specs["max_duration"]]
        
        if specs["channels"] == 1:
            audio = audio.set_channels(1)
        else:
            audio = audio.set_channels(2)
        
        audio = audio.set_frame_rate(specs["sample_rate"])
        
        audio.export(output_path, format=specs["format"], bitrate=specs["bitrate"])
        
        return {
            "duration": len(audio) / 1000.0,
            "format": specs["format"],
            "bitrate": specs["bitrate"],
            "sample_rate": specs["sample_rate"],
            "file_size": os.path.getsize(output_path)
        }
