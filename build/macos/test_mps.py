#!/usr/bin/env python3
"""
Test MPS (Metal Performance Shaders) GPU acceleration on macOS
This script checks if MPS is available and functional
"""

import sys
import time

try:
    import torch
    import torch.nn as nn
except ImportError:
    print("❌ PyTorch is not installed. Please install it first:")
    print("   pip install torch")
    sys.exit(1)


def test_mps_availability():
    """Test if MPS is available on this system."""
    print("=" * 60)
    print("MPS (Metal Performance Shaders) Availability Test")
    print("=" * 60)
    print()

    # Check PyTorch version
    print(f"PyTorch Version: {torch.__version__}")
    print()

    # Check MPS availability
    print("Checking MPS availability...")
    mps_available = torch.backends.mps.is_available()

    if mps_available:
        print("✅ MPS is AVAILABLE on this system")
    else:
        print("❌ MPS is NOT available on this system")
        print()
        print("Possible reasons:")
        print("  • Not running on an Apple Silicon Mac (M1/M2/M3)")
        print("  • macOS version is too old (requires 12.3+)")
        print("  • PyTorch version doesn't support MPS")
        return False

    # Check if MPS is built
    if hasattr(torch.backends.mps, "is_built"):
        print(f"MPS Built: {torch.backends.mps.is_built()}")

    return True


def test_mps_performance():
    """Test MPS performance with a simple computation."""
    print()
    print("=" * 60)
    print("MPS Performance Test")
    print("=" * 60)
    print()

    # Test configuration
    size = 4096
    iterations = 100

    # CPU test
    print("Testing CPU performance...")
    device_cpu = torch.device("cpu")
    a_cpu = torch.randn(size, size, device=device_cpu)
    b_cpu = torch.randn(size, size, device=device_cpu)

    start_time = time.time()
    for _ in range(iterations):
        _ = torch.matmul(a_cpu, b_cpu)
    cpu_time = time.time() - start_time
    print(f"CPU Time: {cpu_time:.3f} seconds")

    # MPS test
    print("Testing MPS performance...")
    device_mps = torch.device("mps")
    a_mps = torch.randn(size, size, device=device_mps)
    b_mps = torch.randn(size, size, device=device_mps)

    # Warm up
    for _ in range(10):
        _ = torch.matmul(a_mps, b_mps)

    start_time = time.time()
    for _ in range(iterations):
        _ = torch.matmul(a_mps, b_mps)
    mps_time = time.time() - start_time
    print(f"MPS Time: {mps_time:.3f} seconds")

    # Compare
    print()
    speedup = cpu_time / mps_time
    print(f"🚀 MPS Speedup: {speedup:.2f}x faster than CPU")

    if speedup > 1.5:
        print("✅ MPS acceleration is working well!")
    elif speedup > 1.0:
        print("⚠️  MPS is faster but speedup is lower than expected")
    else:
        print("❌ MPS is slower than CPU (this shouldn't happen)")


def test_nn_module():
    """Test MPS with a neural network module."""
    print()
    print("=" * 60)
    print("Neural Network on MPS Test")
    print("=" * 60)
    print()

    # Create a simple model
    model = nn.Sequential(nn.Linear(1024, 512), nn.ReLU(), nn.Linear(512, 256), nn.ReLU(), nn.Linear(256, 10))

    device = torch.device("mps")
    model = model.to(device)

    # Test forward pass
    x = torch.randn(32, 1024, device=device)
    y = model(x)

    print(f"Model output shape: {y.shape}")
    print(f"Model device: {next(model.parameters()).device}")
    print("✅ Neural network forward pass successful on MPS")


def get_optimal_device():
    """Get the optimal device for training/inference."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")


def main():
    """Run all MPS tests."""
    print()
    print("🍎 so-vits-svc-fork-osx MPS Test Suite")
    print()

    # Test availability
    if not test_mps_availability():
        print()
        print("Recommended device: CPU")
        sys.exit(1)

    # Test performance
    try:
        test_mps_performance()
    except Exception as e:
        print(f"❌ Performance test failed: {e}")

    # Test neural network
    try:
        test_nn_module()
    except Exception as e:
        print(f"❌ Neural network test failed: {e}")

    # Summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    optimal_device = get_optimal_device()
    print(f"Optimal device for so-vits-svc: {optimal_device}")
    print()

    if optimal_device.type == "mps":
        print("✅ Your system is ready to use MPS acceleration!")
        print("   Make sure to enable 'Use GPU' in the GUI")
    elif optimal_device.type == "cuda":
        print("✅ Your system has CUDA GPU available")
    else:
        print("⚠️  No GPU acceleration available, will use CPU")
        print("   Consider using an Apple Silicon Mac for MPS acceleration")

    print()


if __name__ == "__main__":
    main()
