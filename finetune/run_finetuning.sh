#!/bin/bash

# DeepSeek-V3 Medical Chatbot Fine-tuning Pipeline
# This script automates the complete fine-tuning process

set -e  # Exit on any error

echo "🏥 DeepSeek-V3 Medical Chatbot Fine-tuning Pipeline"
echo "=================================================="

# Configuration
MODEL_NAME="deepseek-ai/DeepSeek-V3"
DATASET_PATH="medical_chatbot_dataset.json"
OUTPUT_DIR="./medical_chatbot_model"
NUM_EXAMPLES=2000
NUM_EPOCHS=3
BATCH_SIZE=4
LEARNING_RATE=2e-4
LORA_R=16
LORA_ALPHA=32

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if CUDA is available
check_cuda() {
    print_status "Checking CUDA availability..."
    if python -c "import torch; print(torch.cuda.is_available())" | grep -q "True"; then
        print_success "CUDA is available"
        GPU_COUNT=$(python -c "import torch; print(torch.cuda.device_count())")
        print_status "Found $GPU_COUNT GPU(s)"
    else
        print_warning "CUDA not available. Training will be slow on CPU."
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Generate training data
generate_data() {
    print_status "Generating training dataset..."
    if [ -f "data_generator.py" ]; then
        python data_generator.py
        if [ -f "$DATASET_PATH" ]; then
            print_success "Training dataset generated: $DATASET_PATH"
        else
            print_error "Failed to generate dataset"
            exit 1
        fi
    else
        print_error "data_generator.py not found"
        exit 1
    fi
}

# Run fine-tuning
run_finetuning() {
    print_status "Starting fine-tuning..."
    print_status "Model: $MODEL_NAME"
    print_status "Output directory: $OUTPUT_DIR"
    print_status "Epochs: $NUM_EPOCHS"
    print_status "Batch size: $BATCH_SIZE"
    print_status "Learning rate: $LEARNING_RATE"
    
    if [ -f "finetune_medical_chatbot.py" ]; then
        python finetune_medical_chatbot.py \
            --model_name "$MODEL_NAME" \
            --dataset_path "$DATASET_PATH" \
            --output_dir "$OUTPUT_DIR" \
            --lora_r "$LORA_R" \
            --lora_alpha "$LORA_ALPHA" \
            --learning_rate "$LEARNING_RATE" \
            --num_epochs "$NUM_EPOCHS" \
            --batch_size "$BATCH_SIZE"
        
        if [ -d "$OUTPUT_DIR" ]; then
            print_success "Fine-tuning completed! Model saved to $OUTPUT_DIR"
        else
            print_error "Fine-tuning failed"
            exit 1
        fi
    else
        print_error "finetune_medical_chatbot.py not found"
        exit 1
    fi
}

# Test the model
test_model() {
    print_status "Testing fine-tuned model..."
    if [ -f "test_medical_chatbot.py" ] && [ -d "$OUTPUT_DIR" ]; then
        python test_medical_chatbot.py --model_path "$OUTPUT_DIR"
        print_success "Model testing completed"
    else
        print_warning "Skipping model testing (test script or model not found)"
    fi
}

# Create model info file
create_model_info() {
    print_status "Creating model information file..."
    cat > "$OUTPUT_DIR/model_info.txt" << EOF
DeepSeek-V3 Medical Chatbot Fine-tuned Model
============================================

Base Model: $MODEL_NAME
Fine-tuning Date: $(date)
Training Examples: $NUM_EXAMPLES
Epochs: $NUM_EPOCHS
Batch Size: $BATCH_SIZE
Learning Rate: $LEARNING_RATE
LoRA Rank: $LORA_R
LoRA Alpha: $LORA_ALPHA

Features:
- Structured medical responses with emojis
- Emergency and non-emergency scenarios
- Voice message processing
- Multilingual support (English/Hindi)
- Medical guidance and recommendations

⚠️  IMPORTANT: This model is for research purposes only.
   Do not use for actual medical diagnosis.
   Always consult healthcare professionals for medical advice.

Usage:
python test_medical_chatbot.py --model_path "$OUTPUT_DIR"
EOF
    print_success "Model information saved to $OUTPUT_DIR/model_info.txt"
}

# Main execution
main() {
    echo ""
    print_status "Starting fine-tuning pipeline..."
    
    # Check system requirements
    check_cuda
    
    # Install dependencies
    install_dependencies
    
    # Generate training data
    generate_data
    
    # Run fine-tuning
    run_finetuning
    
    # Test the model
    test_model
    
    # Create model info
    create_model_info
    
    echo ""
    print_success "🎉 Fine-tuning pipeline completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "  1. Review the model outputs in the test results"
    echo "  2. Check the model_info.txt file for details"
    echo "  3. Use the model for inference or further testing"
    echo ""
    print_warning "Remember: This model is for research purposes only!"
    echo ""
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --data-only    Only generate training data"
        echo "  --train-only   Only run fine-tuning (skip data generation)"
        echo "  --test-only    Only test existing model"
        echo ""
        echo "Environment variables:"
        echo "  MODEL_NAME     Base model name (default: deepseek-ai/DeepSeek-V3)"
        echo "  NUM_EPOCHS     Number of training epochs (default: 3)"
        echo "  BATCH_SIZE     Batch size (default: 4)"
        echo "  LEARNING_RATE  Learning rate (default: 2e-4)"
        echo ""
        exit 0
        ;;
    --data-only)
        print_status "Running data generation only..."
        install_dependencies
        generate_data
        print_success "Data generation completed"
        exit 0
        ;;
    --train-only)
        print_status "Running fine-tuning only..."
        install_dependencies
        run_finetuning
        test_model
        create_model_info
        print_success "Fine-tuning completed"
        exit 0
        ;;
    --test-only)
        print_status "Running model testing only..."
        test_model
        exit 0
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac 