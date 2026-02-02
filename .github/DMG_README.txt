# so-vits-svc OSX Application

Welcome to **so-vits-svc OSX** - Voice conversion software optimized for Apple Silicon with Metal Performance Shaders (MPS) GPU acceleration.

## Installation

### Quick Start
1. Drag **SoVitsSVC-OSX.app** to your Applications folder
2. Launch the application
3. If you see a security warning, go to **System Preferences → Security & Privacy** and click "Open Anyway"

### Alternative Installation
You can also use the **SoVitsSVC-OSX.command** launcher file by double-clicking it.

## Features

- **Apple Metal MPS GPU Acceleration**: Optimized for M1/M2/M3 chips
- **Real-time Voice Conversion**: Convert your voice in real-time with low latency
- **File-based Inference**: Process audio files with high quality
- **Model Training**: Train your own voice models locally
- **Native macOS Experience**: Built specifically for macOS with native UI

## System Requirements

- macOS 11.0 (Big Sur) or later
- Apple Silicon (M1/M2/M3) recommended, Intel Macs supported
- 8GB RAM minimum, 16GB+ recommended for training
- Microphone access for real-time voice conversion

## Getting Started

### For Voice Conversion (Inference)
1. Launch the app
2. Load a pre-trained model (.pth file) and config.json
3. Select input audio or use real-time microphone input
4. Adjust pitch and other parameters
5. Click "Infer" for file conversion or "Start Voice Changer" for real-time

### For Training Models
Training is available via the command-line interface. Open Terminal in the app directory and use:
```bash
# Preprocess audio data
svc pre-resample -i dataset_raw -o dataset/44k

# Generate config
svc pre-config -i dataset/44k

# Extract features
svc pre-hubert -i dataset/44k

# Train model
svc train -c configs/44k/config.json -m logs/44k
```

## Troubleshooting

### "App is damaged" warning
If you see this message, run in Terminal:
```bash
sudo xattr -cr /Applications/SoVitsSVC-OSX.app
```

### MPS/GPU Not Working
The app automatically detects and uses MPS when available. Check the "Use GPU" checkbox in the GUI to enable hardware acceleration.

### Audio Issues
- Grant microphone permissions in System Preferences → Security & Privacy → Privacy → Microphone
- Try different audio devices from the device dropdown menus

## Support

For issues, questions, and contributions, visit:
https://github.com/audiohacking/so-vits-svc-fork-osx

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Note**: This is an unofficial fork of so-vits-svc optimized for macOS with Apple Metal support.
