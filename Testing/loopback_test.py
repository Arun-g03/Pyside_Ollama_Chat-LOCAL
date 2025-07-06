import sounddevice as sd
import numpy as np
from sounddevice import WasapiSettings

print("sounddevice version:", sd.__version__)
print("sounddevice file:", sd.__file__)

samplerate = 44100
blocksize = 2048
target_name = "2- Arctis Nova 7P"

devices = sd.query_devices()
print("\n=== Device List ===")
for idx, dev in enumerate(devices):
    print(f"[{idx}] {dev['name']} (IN:{dev['max_input_channels']} OUT:{dev['max_output_channels']})")
print("==================\n")

found_loopback_device = False

print("Attempting to find a WASAPI loopback compatible device...")

for idx, dev in enumerate(devices):
    # Only test devices whose name contains the target string
    if target_name not in dev['name']:
        continue
    if dev['max_output_channels'] == 0:
        continue
    print(f"\n[TEST] Trying device {idx}: {dev['name']}")
    try:
        # Use WasapiSettings for loopback mode. This is crucial for capturing system audio.
        wasapi_info = WasapiSettings()
        with sd.InputStream(
            device=idx,
            channels=2, # Typically stereo for system audio
            samplerate=samplerate,
            dtype='float32',
            blocksize=blocksize,
            latency='low', # 'low' latency is generally good for responsiveness
            extra_settings=wasapi_info
        ) as stream:
            print(f"  Monitoring device {idx} for 5 blocks...")
            # Read a few blocks to see if any audio data is present
            for i in range(5):
                data, overflowed = stream.read(blocksize)
                maxval = np.max(np.abs(data))
                print(f"    Block {i+1}: Max abs value: {maxval:.6f}") # Formatted for better readability
                
                # A small threshold to detect actual audio, not just noise
                if maxval > 1e-5: 
                    print(f"\n[SUCCESS] Device {idx} ({dev['name']}) is capturing system audio!")
                    found_loopback_device = True
                    break # Found a device, no need to test further blocks for this device
            
            if found_loopback_device:
                break # Found a device, no need to test further devices

    except Exception as e:
        print(f"  [ERROR] Could not test device {idx} ({dev['name']}) for loopback: {e}")


if not found_loopback_device:
    print("\n[FAIL] No output device captured nonzero system audio using WASAPI loopback.")
    print("[INFO] Please ensure audio is currently playing on your system and try again.")
    print("[INFO] If you have multiple audio devices, check your system's default audio output settings.")
else:
    print("\n[INFO] You can use the index of the successfully tested device for WASAPI loopback in your application.")

device_index = ...  # Index of your hardware loopback device (input)
samplerate = 44100
blocksize = 2048

with sd.InputStream(
    device=device_index,
    channels=2,
    samplerate=samplerate,
    dtype='float32',
    blocksize=blocksize
) as stream:
    for _ in range(10):
        data, overflowed = stream.read(blocksize)
        print("Max abs value:", np.max(np.abs(data)))