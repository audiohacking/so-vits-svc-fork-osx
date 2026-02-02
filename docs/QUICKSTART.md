# Quick Start Guide - so-vits-svc OSX

Welcome! This guide will help you get started with so-vits-svc on macOS with Apple Metal MPS GPU acceleration.

## Installation

### Option 1: DMG Installation (Recommended)

1. Download the latest DMG from the [Releases page](https://github.com/audiohacking/so-vits-svc-fork-osx/releases)
2. Open the DMG file
3. Drag **SoVitsSVC-OSX.app** to the Applications folder
4. Launch the app from Applications or Launchpad

### Option 2: Command Line Installation

```bash
pip install so-vits-svc-fork
```

## First Launch

### Security Notice

On first launch, macOS may show a security warning. To open the app:

1. **Method 1**: Right-click the app and select "Open"
2. **Method 2**: Go to System Preferences → Security & Privacy → Click "Open Anyway"
3. **Method 3**: Run in Terminal:
   ```bash
   sudo xattr -cr /Applications/SoVitsSVC-OSX.app
   ```

### Grant Permissions

The app will request:

- **Microphone Access**: Required for real-time voice conversion
- Allow when prompted to use real-time features

## Using the GUI

### Main Interface

When you launch the app, you'll see:

- **Paths Section**: Load your model, config, and optional cluster model
- **Common Section**: Adjust voice conversion parameters
- **File Section**: For converting audio files
- **Realtime Section**: For live microphone conversion
- **Presets Section**: Save and load your settings

### Quick Voice Conversion

#### 1. File Conversion

1. Load a model:
   - Click Browse next to "Model path"
   - Select your `.pth` model file
2. Load config:
   - Click Browse next to "Config path"
   - Select your `config.json` file
3. Select input audio:
   - Click Browse next to "Input audio path"
   - Choose your audio file
4. Click **Infer** to convert
5. Output will be saved automatically

#### 2. Real-time Conversion

1. Load model and config (same as above)
2. Select your microphone from "Input device"
3. Select your speakers/headphones from "Output device"
4. Adjust **Block seconds** (0.5 is a good start)
5. Click **Start Voice Changer**
6. Speak into your microphone!
7. Click **Stop Voice Changer** when done

### Important Settings

#### GPU Acceleration

- Enable **"Use GPU"** checkbox (should be on by default)
- This uses Apple Metal MPS for faster processing
- Test if it's working: Run `python build/macos/test_mps.py`

#### Pitch/Transpose

- **Auto predict F0**: Automatic pitch detection (recommended for files)
- **Pitch**: Manual pitch adjustment (in semitones, 12 = 1 octave)
- Turn OFF auto predict F0 for real-time for stability

#### Quality Settings

- **Silence threshold**: Adjust if input audio is too quiet/loud (-20 to -40 dB)
- **F0 prediction method**:
  - `dio`: Fast, good for real-time
  - `crepe`: Best quality, slower
  - `harvest`: Balanced

## Training Your Own Model

Training is done via command line. Open Terminal and navigate to your project folder:

### Step 1: Prepare Dataset

```bash
# Create dataset folder structure
mkdir -p dataset_raw/your_speaker_name

# Add your audio files (WAV format recommended)
# Place 10-30 minutes of clean speech in that folder
```

### Step 2: Preprocess

```bash
# Resample audio to 44.1kHz
svc pre-resample -i dataset_raw -o dataset/44k

# Generate configuration
svc pre-config -i dataset/44k

# Extract features (this will take time)
svc pre-hubert -i dataset/44k
```

### Step 3: Train

```bash
# Start training
svc train -c configs/44k/config.json -m logs/44k

# With TensorBoard monitoring (optional)
svc train -c configs/44k/config.json -m logs/44k --tensorboard
```

Training time varies:

- **Apple Silicon (M1/M2/M3)**: ~2-6 hours with MPS
- **Intel Mac**: ~6-24 hours on CPU

### Step 4: Use Your Model

Once training is complete:

1. Your model is in `logs/44k/G_XXXXX.pth`
2. Config is in `configs/44k/config.json`
3. Load these in the GUI and start converting!

## Tips & Tricks

### Getting Best Quality

1. Use high-quality input audio (clean, no noise)
2. For training: 10-30 minutes of varied speech
3. Use `crepe` F0 method for best results
4. Adjust pitch carefully - start with 0 and adjust by ear

### Real-time Performance

1. Lower **Block seconds** = lower latency, less stable
2. Higher **Block seconds** = higher latency, more stable
3. Use `dio` F0 method for lowest latency
4. Turn OFF **Auto predict F0** for real-time

### Troubleshooting

- **Choppy audio**: Increase Block seconds or Silence threshold
- **Too much latency**: Decrease Block seconds
- **Poor quality**: Use better input audio, try crepe method
- **Out of memory**: Lower Max chunk seconds

## Advanced Features

### Cluster Models

For better speaker similarity:

```bash
# Train k-means cluster
svc train-cluster -i dataset/44k -o logs/44k/kmeans.pt

# Load in GUI and adjust "Cluster infer ratio" (0.0-1.0)
```

### Presets

1. Configure your favorite settings
2. Enter a name in "Preset name"
3. Click "Add current settings as a preset"
4. Select from dropdown to load later

## Getting Help

### Common Issues

- **"App is damaged"**: Run `sudo xattr -cr /Applications/SoVitsSVC-OSX.app`
- **No microphone**: Grant permissions in System Preferences
- **MPS not working**: Check with `python build/macos/test_mps.py`
- **Training slow**: Ensure GPU checkbox is enabled

### Resources

- [GitHub Repository](https://github.com/audiohacking/so-vits-svc-fork-osx)
- [Build Documentation](BUILD_MACOS.md)
- [Original so-vits-svc](https://github.com/svc-develop-team/so-vits-svc)

### Support

- Open an issue on GitHub
- Check existing issues for solutions
- Share your feedback!

## Updates

To update to a new version:

1. Download the latest DMG
2. Replace the app in Applications folder
3. Your settings and presets are preserved

---

**Enjoy voice conversion on macOS! 🎵🍎**
