transcription_app/
├── data/                      # Input and output files
│   ├── input/                 # Store video/audio files
│   └── output/                # Store transcriptions
├── models/                    # Whisper model weights
├── src/                       # Source code
│   ├── gui/                   # PyQt5 GUI files
│   │   ├── __init__.py        # Init for GUI module
│   │   └── main_window.py     # Main PyQt5 window
│   ├── core/                  # Core logic
│   │   ├── __init__.py        # Init for core module
│   │   ├── transcription.py   # Logic for Whisper integration
│   │   └── utils.py           # Helper functions (e.g., FFmpeg)
│   └── main.py                # Entry point for the application
├── tests/                     # Test cases
│   ├── test_transcription.py  # Unit tests for transcription logic
│   ├── test_utils.py          # Unit tests for helper functions
│   └── sample_files/          # Files for testing
├── env/                       # Environment files
│   ├── conda.yaml             # Conda environment specification
│   └── requirements.txt       # Optional: pip requirements for portability
├── logs/                      # Log files
├── README.md                  # Documentation
└── LICENSE                    # Licensing information (optional)
---

## Create conda environment:

```
cd transcription_app/env
conda env create -f conda.yaml
conda activate transcription_app
```

## Ensure dependencies are installed correctly:

- Check PyTorch and CUDA:
```
python -c "import torch; print(torch.cuda.is_available())"
```

- Check FFmpeg:
```
ffmpeg -version

```

## Test the Script:

- Place a sample video file (example.mp4) in data/input/.

- ***Run the script from the src directory:***
```
cd transcription_app/src
python core/transcription.py
```

- Verify the transcription output in data/output/transcription.txt.

## Install FLAN-T5 and BART

- Download pretrained weights from Hugging Face for both models:
```
# FLAN-T5
transformers-cli download google/flan-t5-large

# BART
transformers-cli download facebook/bart-large-cnn
```


