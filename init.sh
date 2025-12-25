#!/bin/bash

# LeRobot Environment Initialization Script

echo "🤖 LeRobot Environment Setup"
echo "=============================="

# 1. Check/Activate Conda Environment
# Note: In a script, 'conda activate' might not work directly unless conda hook is sourced.
# We'll try to detect if we are in the 'lerobot' env.

CURRENT_ENV=$(echo $CONDA_DEFAULT_ENV)
TARGET_ENV="lerobot"

if [ "$CURRENT_ENV" != "$TARGET_ENV" ]; then
    echo "⚠️  Current environment is '$CURRENT_ENV', but 'lerobot' is recommended."

    # Try to find conda base
    CONDA_BASE=$(conda info --base 2>/dev/null)
    if [ -n "$CONDA_BASE" ]; then
        source "$CONDA_BASE/etc/profile.d/conda.sh"
        conda activate $TARGET_ENV
        if [ $? -eq 0 ]; then
            echo "✅ Successfully activated '$TARGET_ENV' environment."
        else
            echo "❌ Failed to activate '$TARGET_ENV'. Please run 'conda activate $TARGET_ENV' manually."
            # We don't exit here, just warn, in case user uses a different env name.
        fi
    else
         echo "❌ Conda not found or not initialized in shell."
    fi
else
    echo "✅ Already in '$TARGET_ENV' environment."
fi

echo "------------------------------"

# 2. Check and Install Dependencies

echo "📦 Checking dependencies..."

# Function to check import
check_import() {
    python -c "import $1" 2>/dev/null
    return $?
}

# Core LeRobot check
if ! check_import "lerobot"; then
    echo "⚠️  'lerobot' package not found. Installing in editable mode..."
    pip install -e ./lerobot
else
    echo "✅ 'lerobot' core package is installed."
fi

# Libero check (requires special handling for egl_probe)
if ! check_import "libero"; then
    echo "⚠️  'libero' module not found. Installing [libero] extras..."

    # Install prebuilt hf-egl-probe first to avoid compilation issues
    pip install 'hf-egl-probe>=1.0.1' 2>/dev/null || echo "  (hf-egl-probe may already be installed)"

    # Install libero extras
    pip install -e "./lerobot[libero]" || {
        echo "  ⚠️  Standard installation failed. Trying manual dependency installation..."
        pip install 'hf-libero>=0.1.3,<0.2.0' --no-deps
        pip install 'bddl==1.0.1' easydict 'hydra-core>=1.2,<1.4' thop transformers tensorboardX
        pip install 'robosuite==1.4.0'
    }
else
    echo "✅ 'libero' module is installed."
fi

# Aloha check
if ! check_import "gym_aloha"; then
    echo "⚠️  'gym_aloha' not found. Installing [aloha] extras..."
    pip install -e "./lerobot[aloha]"
else
    echo "✅ 'gym_aloha' is installed."
fi

# PushT check
if ! check_import "gym_pusht"; then
    echo "⚠️  'gym_pusht' not found. Installing [pusht] extras..."
    pip install -e "./lerobot[pusht]"
else
    echo "✅ 'gym_pusht' is installed."
fi

# Safetensors check (for our fix)
if ! check_import "safetensors"; then
    echo "Installing safetensors..."
    pip install safetensors
fi

# num2words check (for SmolVLA)
if ! check_import "num2words"; then
    echo "⚠️  'num2words' not found (required for SmolVLA). Installing..."
    pip install num2words
else
    echo "✅ 'num2words' is installed."
fi

# Pi0/Pi0.5 special check
echo "------------------------------"
echo "🔍 Checking configuration for Pi0/Pi0.5 models..."
# Check if current transformers version supports Pi models (simplified check)
TRANSFORMERS_VERSION=$(python -c "import transformers; print(transformers.__version__)" 2>/dev/null)
echo "   Current transformers version: $TRANSFORMERS_VERSION"

# Default to installing Pi-compatible transformers if not already on the correct branch/version
# We check if it's the standard PyPI version (usually simple X.Y.Z) vs the git version
# A robust check is hard, so we'll just force install if --no-pi is NOT passed, to be safe for Pi users.
# But to avoid re-installing every time, we can check if it looks 'patched' or if user explicitly asks.
# User requested "default to --pi".

if [[ "$1" == "--no-pi" ]]; then
    echo "ℹ️  Skipping Pi-compatible transformers installation (--no-pi specified)."
else
    # Check if we should reinstall (simple heuristic: if version doesn't look like 4.53.3 which is what the patch branch is currently based on, or just force it)
    # To be safe and ensure Pi0 works out of the box, we'll install it unless it's already there.
    # Since checking is complex, we will just run the install. pip will skip if already satisfied (mostly).
    # But git installs are slow to check.

    echo "📦 Ensuring Pi-compatible transformers (fix/lerobot_openpi) is installed..."
    # We use pip freeze to check if it is installed from git
    if pip freeze | grep -q "transformers @ git+https://github.com/huggingface/transformers.git@fix/lerobot_openpi"; then
         echo "✅ Pi-compatible transformers is already installed."
    else
         echo "⚠️  Installing Pi-compatible transformers..."
         pip uninstall -y transformers 2>/dev/null
         pip install "git+https://github.com/huggingface/transformers.git@fix/lerobot_openpi"
         echo "✅ Switched to Pi-compatible transformers."
    fi
fi

echo "------------------------------"
echo "🎉 Setup complete! You are ready to run LeRobot examples."
echo ""
echo "Try running:"
echo "  python lerobot/src/lerobot/scripts/lerobot_eval.py --policy.path=lerobot/pi0_libero_finetuned --env.type=libero --env.task=libero_10 --eval.batch_size=1 --eval.n_episodes=5 --policy.device=cuda"
