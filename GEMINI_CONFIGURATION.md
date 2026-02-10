# Google Gemini 3 Configuration Guide

## Why Google Gemini 3?

AutoMate Studio uses **Google Gemini 3 Flash Preview** as its primary LLM for several key reasons:

### Advantages

1. **⚡ Speed**: Gemini 3 Flash is optimized for low-latency responses
2. **🎯 Quality**: Advanced reasoning with built-in "thinking" mechanism
3. **💰 Cost-Effective**: Competitive pricing for cloud-based LLM
4. **🔄 Reliability**: Google Cloud infrastructure ensures high availability
5. **🆕 Latest Features**: Access to cutting-edge AI capabilities
6. **🌐 No Local Setup**: No need to install or run local LLM servers

### Native Thinking Mechanism

Gemini 3 introduces a native **thinking_level** parameter that replaces manual Chain of Thought prompting:

- `thinking_level="low"` - Fast responses for simple tasks
- `thinking_level="medium"` - Balanced for most workflows
- `thinking_level="high"` - Deep reasoning for complex problems

---

## Getting Your API Key

### Step 1: Access Google AI Studio

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**

### Step 2: Create API Key

1. Click **"Create API key in new project"** (recommended)
   - Or select an existing Google Cloud project
2. Your API key will be generated instantly
3. **Copy the key immediately** - you won't be able to see it again!

### Step 3: Add to Environment

Open your `.env` file and add:

```env
GOOGLE_API_KEY=AIzaSy... # Your actual API key here
```

---

## Configuration in AutoMate

### Current Setup

All RAG components use Gemini 3 Flash Preview:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1.0,              # Recommended by Google
    thinking_level="medium",      # Adjust based on task complexity
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

### Files Using Gemini

- `RAG/generator.py` - Main text generation (thinking_level="medium")
- `RAG/grader1.py` - Document relevance (thinking_level="low")
- `RAG/grader2.py` - Answer quality (thinking_level="low")
- `RAG/hallucinate_detector.py` - Fact checking (thinking_level="low")
- `RAG/answer_rewriter.py` - Query transformation (thinking_level="medium")
- `RAG/router.py` - Query routing (thinking_level="low")

---

## Testing Your Setup

### Quick Test

```powershell
cd C:\Users\amloul\Documents\autoMate

# Test API connection
uv run python -c "from langchain_google_genai import ChatGoogleGenerativeAI; import os; from dotenv import load_dotenv; load_dotenv(); llm = ChatGoogleGenerativeAI(model='gemini-3-flash-preview', google_api_key=os.getenv('GOOGLE_API_KEY')); print(llm.invoke('Hello, Gemini!'))"
```

Expected output:
```
Hello! How can I help you today?
```

### Full RAG Test

```powershell
# Run a single RAG component
uv run python -c "from RAG.generator import llm; print(llm.invoke('What is automation?'))"
```

---

## Troubleshooting

### ❌ "Invalid API Key"

**Problem**: Authentication failed

**Solution**:
```powershell
# Verify key is set
echo $env:GOOGLE_API_KEY  # PowerShell
# or
echo $GOOGLE_API_KEY      # Bash

# Check .env file
cat .env | Select-String "GOOGLE_API_KEY"
```

### ❌ "Quota Exceeded"

**Problem**: You've exceeded your API quota

**Solution**:
- Check your [Google Cloud Console](https://console.cloud.google.com/)
- Navigate to **APIs & Services** → **Quotas**
- Request quota increase if needed
- Or wait for quota reset (usually monthly)

### ❌ "Model Not Found"

**Problem**: Model name incorrect

**Solution**:
- Verify you're using: `gemini-3-flash-preview` or `gemini-3-pro-preview`
- These are preview models - names may change
- Check [Google AI Studio](https://ai.google.dev/) for current model names

---

## Models Explained

### Available Models

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| **gemini-3-flash-preview** | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | 💰 Low | Current default |
| **gemini-3-pro-preview** | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | 💰💰 Medium | Complex reasoning |

### Switching Models

Edit any RAG file to change the model:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",  # Change here
    temperature=1.0,
    thinking_level="high",          # Increase for Pro
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

---

## Advanced Configuration

### Temperature Settings

```python
# More deterministic (consistent outputs)
temperature=0.3

# Balanced (recommended)
temperature=1.0

# More creative (varied outputs)
temperature=1.5
```

### Thinking Levels

```python
# Fast, simple tasks
thinking_level="low"

# General purpose (default)
thinking_level="medium"

# Complex reasoning, analysis
thinking_level="high"
```

### Custom Configuration

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1.0,
    thinking_level="medium",
    max_output_tokens=2048,           # Limit response length
    top_p=0.95,                       # Nucleus sampling
    top_k=40,                         # Top-k sampling
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

---

## Cost Estimation

### Gemini 3 Flash Preview Pricing

*(Prices as of February 2026 - check Google AI Pricing for current rates)*

- **Input**: ~$0.0001 per 1K tokens
- **Output**: ~$0.0003 per 1K tokens

### Typical Usage

A single workflow analysis with:
- 3 PDF documents (~10 pages each)
- 5 automation opportunities
- Full workflow generation

**Estimated cost**: $0.01 - $0.05 per analysis

---

## Switching Back to Ollama (Optional)

If you prefer local LLM inference:

1. **Install Ollama**: [ollama.ai](https://ollama.ai)
2. **Pull model**: `ollama pull llama3.2`
3. **Update RAG files**:

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    format="json"  # For structured output
)
```

---

## Resources

- **Google AI Studio**: https://makersuite.google.com/
- **Gemini API Docs**: https://ai.google.dev/docs
- **Pricing**: https://ai.google.dev/pricing
- **Model Cards**: https://ai.google.dev/models/gemini

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Verify your API key at [Google AI Studio](https://makersuite.google.com/)
3. Open an issue on [GitHub](https://github.com/your-username/automate-studio/issues)
4. Contact support: your-email@example.com

---

**Last Updated**: February 10, 2026
