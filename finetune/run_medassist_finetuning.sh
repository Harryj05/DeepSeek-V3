#!/bin/bash

# MedAssist AI - DeepSeek-V3 Fine-tuning Pipeline
# Complete automation for the MedAssist AI healthcare platform

set -e  # Exit on any error

echo "🏥 MedAssist AI - DeepSeek-V3 Fine-tuning Pipeline"
echo "=================================================="
echo "Comprehensive Healthcare Intelligence Platform"
echo "From WhatsApp to Full-Scale Health Management"
echo

# Configuration
MODEL_NAME="deepseek-ai/DeepSeek-V3"
DATASET_PATH="medassist_ai_dataset.json"
OUTPUT_DIR="./medassist_ai_model"
NUM_EXAMPLES=3000
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
    print_status "Installing MedAssist AI dependencies..."
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
    print_status "Generating MedAssist AI training dataset..."
    if [ -f "medassist_data_generator.py" ]; then
        python medassist_data_generator.py
        if [ -f "$DATASET_PATH" ]; then
            print_success "Training dataset generated: $DATASET_PATH"
        else
            print_error "Failed to generate dataset"
            exit 1
        fi
    else
        print_error "medassist_data_generator.py not found"
        exit 1
    fi
}

# Run fine-tuning
run_finetuning() {
    print_status "Starting MedAssist AI fine-tuning..."
    print_status "Model: $MODEL_NAME"
    print_status "Output directory: $OUTPUT_DIR"
    print_status "Epochs: $NUM_EPOCHS"
    print_status "Batch size: $BATCH_SIZE"
    print_status "Learning rate: $LEARNING_RATE"
    print_status "Training examples: $NUM_EXAMPLES"
    
    if [ -f "finetune_medassist_ai.py" ]; then
        python finetune_medassist_ai.py \
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
        print_error "finetune_medassist_ai.py not found"
        exit 1
    fi
}

# Test the model
test_model() {
    print_status "Testing MedAssist AI model..."
    if [ -f "test_medassist_ai.py" ]; then
        python test_medassist_ai.py
        print_success "Model testing completed"
    else
        print_warning "Skipping model testing (test script not found)"
    fi
}

# Create model info file
create_model_info() {
    print_status "Creating MedAssist AI model information file..."
    cat > "$OUTPUT_DIR/medassist_ai_info.txt" << EOF
MedAssist AI - DeepSeek-V3 Fine-tuned Model
===========================================

Platform: Comprehensive Healthcare Intelligence
Base Model: $MODEL_NAME
Fine-tuning Date: $(date)
Training Examples: $NUM_EXAMPLES
Epochs: $NUM_EPOCHS
Batch Size: $BATCH_SIZE
Learning Rate: $LEARNING_RATE
LoRA Rank: $LORA_R
LoRA Alpha: $LORA_ALPHA

🏥 Key Features:
• WhatsApp Bot Integration
• Emergency Response System
• Voice Message Processing
• Medication Management
• Health Tips & Education
• Web App Transition
• Family Care Coordination
• Corporate Wellness Management
• Multilingual Support (English, Hindi, Tamil, Bengali)

🎯 User Segments:
• Rural Health Seekers
• Urban Professionals
• Health-Conscious Families
• Chronic Disease Patients
• Healthcare Providers
• Corporate Wellness Programs

💰 Revenue Model:
• Free Tier: Healthcare partnerships
• Premium: Individual (₹299/month), Family (₹499/month)
• Corporate: ₹99/employee/month
• B2B: Provider tools, API licensing

🚀 Go-to-Market:
• Phase 1: WhatsApp bot launch
• Phase 2: Web platform expansion
• Phase 3: Corporate wellness & B2B

⚠️  IMPORTANT: This model is for research purposes only.
   Do not use for actual medical diagnosis.
   Always consult healthcare professionals for medical advice.

Usage:
python test_medassist_ai.py
python medassist_demo.py --mode comprehensive
EOF
    print_success "Model information saved to $OUTPUT_DIR/medassist_ai_info.txt"
}

# Main execution
main() {
    echo ""
    print_status "Starting MedAssist AI fine-tuning pipeline..."
    
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
    print_success "🎉 MedAssist AI fine-tuning pipeline completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "  1. Review the model outputs in the test results"
    echo "  2. Check the medassist_ai_info.txt file for details"
    echo "  3. Use the model for inference or further testing"
    echo "  4. Deploy to WhatsApp Business API"
    echo "  5. Integrate with web application"
    echo ""
    print_warning "Remember: This model is for research purposes only!"
    echo ""
    print_status "MedAssist AI - From WhatsApp to Full-Scale Health Management"
    echo "🏥 AI-Powered Healthcare for Every Indian 🏥"
    echo ""
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "MedAssist AI - DeepSeek-V3 Fine-tuning Pipeline"
        echo "Comprehensive Healthcare Intelligence Platform"
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
        echo "Features:"
        echo "  • WhatsApp Bot Integration"
        echo "  • Emergency Response System"
        echo "  • Voice Message Processing"
        echo "  • Medication Management"
        echo "  • Health Tips & Education"
        echo "  • Web App Transition"
        echo "  • Family Care Coordination"
        echo "  • Corporate Wellness Management"
        echo "  • Multilingual Support"
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