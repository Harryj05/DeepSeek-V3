# DeepSeek-V3 Medical Chatbot Fine-tuning

This directory contains the complete fine-tuning setup for creating a medical chatbot based on DeepSeek-V3 that responds in a specific structured format with emojis, medical alerts, and guidance.

## 🏥 Medical Response Format

The fine-tuned model will respond in the following structured format:

### Yellow Alert (Non-Emergency)
```
⚠
YELLOW ALERT - Medical Attention Recommended
📋
Possible Conditions:
• Viral fever (most likely)
• Seasonal flu
• COVID-19 (get tested)
🏥
Immediate Actions:
• Rest and hydrate
• Paracetamol for fever
• Monitor temperature
⚠
See doctor if:
• Fever >101°F for >3 days
• Breathing difficulty
• Severe weakness
🏥
Nearby Options:
• Dr. Sharma Clinic - 2km (₹200)
• City Hospital - 5km (₹500)
• Call: 102 (Ambulance)
Need more detailed analysis? Check our web app: [link]
```

### Emergency Response
```
🚨
HEART EMERGENCY - ACT NOW!
🏥
CALL IMMEDIATELY:
• 108 - Emergency Ambulance
• 102 - Medical Emergency
⏰
WHILE WAITING:
• Sit down, don't lie flat
• Chew aspirin if available
• Stay calm, help is coming
📍
Share location with family/friends
  I'm monitoring - reply if condition changes
```

### Voice Message Processing
```
🎤
Voice received! Processing...
I understood: "Stomach pain" Is this correct?
✅
Yes
❌
No (type correct symptom)
```

## 📁 File Structure

```
finetune/
├── requirements.txt              # Dependencies for fine-tuning
├── medical_response_templates.py # Response templates and formatting
├── data_generator.py            # Training data generation
├── finetune_medical_chatbot.py  # Main fine-tuning script
├── test_medical_chatbot.py      # Testing and evaluation script
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd finetune
pip install -r requirements.txt
```

### 2. Generate Training Data

```bash
python data_generator.py
```

This will create `medical_chatbot_dataset.json` with 2000 training examples covering:
- Fever scenarios
- Emergency situations
- Voice message processing
- General medical advice

### 3. Fine-tune the Model

```bash
python finetune_medical_chatbot.py \
    --model_name "deepseek-ai/DeepSeek-V3" \
    --dataset_path "medical_chatbot_dataset.json" \
    --output_dir "./medical_chatbot_model" \
    --num_epochs 3 \
    --batch_size 4 \
    --learning_rate 2e-4
```

### 4. Test the Fine-tuned Model

```bash
python test_medical_chatbot.py --model_path "./medical_chatbot_model"
```

## ⚙️ Configuration Options

### Fine-tuning Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--model_name` | `deepseek-ai/DeepSeek-V3` | Base model to fine-tune |
| `--dataset_path` | `medical_chatbot_dataset.json` | Training dataset path |
| `--output_dir` | `./medical_chatbot_model` | Output directory |
| `--lora_r` | `16` | LoRA rank |
| `--lora_alpha` | `32` | LoRA alpha |
| `--learning_rate` | `2e-4` | Learning rate |
| `--num_epochs` | `3` | Number of training epochs |
| `--batch_size` | `4` | Batch size |
| `--max_seq_length` | `2048` | Maximum sequence length |

### Hardware Requirements

- **GPU**: NVIDIA GPU with at least 24GB VRAM (A100, H100, or similar)
- **RAM**: 64GB+ system RAM
- **Storage**: 100GB+ free space for model weights and training data

## 🏗️ Architecture

### LoRA Fine-tuning
- Uses Parameter Efficient Fine-tuning (PEFT) with LoRA
- Only trains ~1% of model parameters
- Maintains model performance while reducing memory usage

### Training Data Structure
```json
{
  "messages": [
    {"role": "user", "content": "I have fever"},
    {"role": "assistant", "content": "⚠\nYELLOW ALERT - Medical Attention Recommended\n..."}
  ],
  "category": "fever"
}
```

### Response Templates
The model learns to generate responses using predefined templates:
- **Yellow Alert**: For non-emergency medical situations
- **Emergency Response**: For critical medical situations
- **Voice Processing**: For handling voice messages
- **Symptom Analysis**: For detailed symptom assessment

## 🧪 Testing Scenarios

The test script covers:

1. **Fever Scenarios**: English and Hindi inputs
2. **Emergency Situations**: Heart attack, breathing difficulty
3. **Voice Messages**: Hindi and English voice processing
4. **Medical Advice**: Diabetes, hypertension guidance
5. **Custom Scenarios**: Various medical symptoms

## 📊 Expected Performance

After fine-tuning, the model should:

- ✅ Generate responses in the exact structured format
- ✅ Use appropriate emojis and medical terminology
- ✅ Provide relevant medical guidance
- ✅ Handle multilingual inputs (English/Hindi)
- ✅ Maintain medical accuracy and safety

## 🔧 Customization

### Adding New Medical Scenarios

1. **Update Templates**: Add new response templates in `medical_response_templates.py`
2. **Generate Data**: Add new conversation patterns in `data_generator.py`
3. **Retrain**: Run the fine-tuning script with updated data

### Modifying Response Format

Edit the template functions in `medical_response_templates.py` to change:
- Emoji usage
- Text formatting
- Medical terminology
- Response structure

## ⚠️ Important Notes

### Medical Disclaimer
This is a research project. The fine-tuned model:
- Should NOT be used for actual medical diagnosis
- Is for educational and research purposes only
- Does not replace professional medical advice
- May contain inaccuracies

### Safety Considerations
- Always include medical disclaimers in production use
- Implement proper medical content filtering
- Ensure compliance with healthcare regulations
- Add emergency contact information

### Model Limitations
- Limited to training data scenarios
- May not handle all medical situations
- Requires human oversight for medical accuracy
- Should be validated by medical professionals

## 🤝 Contributing

To improve the medical chatbot:

1. **Expand Training Data**: Add more medical scenarios
2. **Improve Templates**: Enhance response formatting
3. **Add Validation**: Implement medical accuracy checks
4. **Test Thoroughly**: Validate with medical professionals

## 📚 References

- [DeepSeek-V3 Paper](https://arxiv.org/abs/2412.19437)
- [PEFT Documentation](https://huggingface.co/docs/peft)
- [TRL Documentation](https://huggingface.co/docs/trl)
- [Medical Chatbot Guidelines](https://www.who.int/health-topics/digital-health)

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Check the DeepSeek-V3 documentation
- Review the fine-tuning logs for debugging

---

**Note**: This fine-tuning setup is designed for research and educational purposes. Always consult with medical professionals for actual medical advice. 