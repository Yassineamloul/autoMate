<div align="center">

# 🤖 AutoMate Studio

### AI-Powered Automation Discovery & Workflow Generation

**Transform your business documents into production-ready n8n workflows instantly**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Documentation](#-documentation) • [Architecture](#-architecture)

<img src="https://img.shields.io/badge/RAG-Enabled-purple.svg" alt="RAG Enabled" />
<img src="https://img.shields.io/badge/LangChain-Powered-orange.svg" alt="LangChain" />
<img src="https://img.shields.io/badge/n8n-Integration-brightgreen.svg" alt="n8n" />

</div>

---

## 🎯 What is AutoMate Studio?

**AutoMate Studio** is an intelligent automation discovery platform that uses **Retrieval-Augmented Generation (RAG)** and **LangGraph** to analyze your business documents, identify automation opportunities, and automatically generate production-ready n8n workflows.

### The Problem It Solves

Traditional automation requires:
- ❌ Manual identification of repetitive tasks
- ❌ Technical expertise in workflow design
- ❌ Hours of configuration and testing
- ❌ Deep knowledge of n8n nodes and connections

### The AutoMate Solution

- ✅ **Automatic Discovery**: AI analyzes documents to find automation opportunities
- ✅ **Intelligent Prioritization**: Ranks opportunities by impact and feasibility
- ✅ **One-Click Generation**: Creates complete n8n workflows instantly
- ✅ **Production-Ready**: Generates tested, deployable workflow JSON

---

## ✨ Features

### 🧠 AI-Powered Analysis
- **RAG-Based Document Understanding**: Deeply analyzes PDFs, CSVs, and web content
- **Smart Context Extraction**: Understands business processes from documentation
- **Multi-Document Correlation**: Identifies patterns across multiple sources

### 🎨 Modern User Experience
- **Beautiful Glassmorphism UI**: Dark mode interface with smooth animations
- **Real-Time Progress Tracking**: Live updates during analysis and generation
- **Interactive Opportunity Selection**: Review and choose automation scenarios
- **Drag-and-Drop Upload**: Effortless document management

### 🔄 Intelligent Workflow Generation
- **n8n Node Architecture**: Creates proper node structures with correct types
- **Connection Logic**: Establishes proper data flow between nodes
- **Error Handling**: Includes retry logic and fallback mechanisms
- **Best Practices**: Follows n8n conventions and patterns

### 📊 Smart Prioritization
- **Impact Scoring**: Ranks opportunities by potential business value
- **Feasibility Assessment**: Considers technical complexity
- **Department Mapping**: Identifies which teams benefit most

---

## 🚀 Quick Start

### One-Click Launch (Recommended)

```powershell
# Clone the repository
git clone https://github.com/your-username/automate-studio.git
cd automate-studio

# Install dependencies
uv sync
cd web && npm install && cd ..

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Launch both servers
.\start_fullstack.ps1
```

**Access the application:**
- 🌐 Web Interface: **http://localhost:3000**
- 📖 API Documentation: **http://localhost:8000/docs**

> 📘 **New to Google Gemini?** Check out our [Gemini Configuration Guide](GEMINI_CONFIGURATION.md) for detailed setup instructions, troubleshooting, and best practices.

### Manual Launch

**Terminal 1 - API Server:**
```powershell
.\start_api.ps1
```

**Terminal 2 - Web Interface:**
```powershell
cd web
npm run dev
```

---

## 📦 Installation

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.12+ | Backend runtime |
| **Node.js** | 18+ | Frontend runtime |
| **uv** | Latest | Python package manager |
| **Google Gemini API** | - | AI/LLM inference (Cloud-based) |

### Step 1: Install System Dependencies

```powershell
# Install uv (Python package manager)
pip install uv

# Get Google Gemini API Key (Required)
# Visit: https://makersuite.google.com/app/apikey
# Click "Get API Key" and copy your key
```

### Step 2: Clone and Setup Project

```powershell
# Clone repository
git clone https://github.com/your-username/automate-studio.git
cd automate-studio

# Install Python dependencies
uv sync

# Install frontend dependencies
cd web
npm install
cd ..
```

### Step 3: Configure Environment

```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env file
notepad .env
```

**Required Environment Variables:**

```env
# Google Gemini API (Required - for AI/LLM processing)
GOOGLE_API_KEY=your-google-gemini-api-key

# n8n Configuration
N8N_BASE_URL=https://your-instance.app.n8n.cloud
N8N_API_KEY=your-n8n-api-key

# Context7 API (for n8n documentation access)
CONTEXT7_API_KEY=your-context7-api-key
```

**Where to get API keys:**

1. **GOOGLE_API_KEY** (Required) - Google Gemini 3 API
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Click **"Get API Key"** or **"Create API Key"**
   - Copy your API key
   - Paste it in your `.env` file: `GOOGLE_API_KEY=your-key-here`
   - **Important**: This key is required for the AI analysis to work

2. **N8N_API_KEY** - n8n Cloud API
   - Log in to your [n8n Cloud](https://n8n.io/) instance
   - Go to **Settings** → **API**
   - Generate a new API key
   - Copy and paste it in your `.env` file

3. **CONTEXT7_API_KEY** - Context7 API for n8n documentation
   - Visit [Context7 Dashboard](https://context7.com)
   - Sign up or log in
   - Generate an API key
   - Paste it in your `.env` file

### Step 4: Verify Installation

```powershell
# Test Python environment
uv run python -c "import fastapi; print('✅ FastAPI installed')"

# Test Google Gemini integration
uv run python -c "from langchain_google_genai import ChatGoogleGenerativeAI; import os; from dotenv import load_dotenv; load_dotenv(); print('✅ Gemini API configured' if os.getenv('GOOGLE_API_KEY') else '❌ GOOGLE_API_KEY not found in .env')"

# Test Node
npm --version
```

---

## 🎯 How to Use

### 1️⃣ Upload Documents

<img src="docs/images/upload.png" alt="Upload Interface" width="600" />

- **Drag and drop** PDF or CSV files (max 10MB each)
- **Optional**: Add a context URL for additional information
- Click **"Analyze & Find Opportunities"**

### 2️⃣ AI Analysis Phase

The system performs:
1. **Document Ingestion**: Parses PDFs/CSVs and extracts text
2. **RAG Indexing**: Creates vector embeddings for semantic search
3. **Opportunity Mining**: AI identifies automation candidates
4. **Impact Assessment**: Scores and ranks opportunities

### 3️⃣ Select Automation Scenario

<img src="docs/images/opportunities.png" alt="Opportunity Selection" width="600" />

Review discovered opportunities:
- **Title**: What will be automated (e.g., "Invoice Processing Workflow")
- **Priority Score**: 1-10 ranking based on impact
- **Department**: Team that benefits (Finance, HR, IT, etc.)
- **Description**: Details about the automation

Click on your preferred opportunity to proceed.

### 4️⃣ Workflow Generation

The AI architect:
1. **Analyzes Requirements**: Understands the automation goal
2. **Plans Architecture**: Designs node structure and flow
3. **Generates Code**: Creates n8n-compatible JSON
4. **Validates Output**: Ensures workflow integrity

### 5️⃣ Deploy or Download

**Option A - Direct Deployment:**
- If `N8N_BASE_URL` is configured
- Workflow is deployed automatically
- Opens in your n8n instance

**Option B - Manual Import:**
- Download JSON file
- Import in n8n: **Workflows → Import → From File**

---

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (Next.js)                │
│         Modern React App with Real-Time Updates             │
│                     Port: 3000                               │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
                         │ (JSON Communication)
┌────────────────────────▼────────────────────────────────────┐
│                  FastAPI Backend Server                      │
│           Async Python Server with CORS Support             │
│                     Port: 8000                               │
└────────┬──────────────────────────────────┬─────────────────┘
         │                                  │
         │ Invokes                          │ Manages
         │                                  │
┌────────▼────────────┐          ┌─────────▼──────────────────┐
│   graph.py          │          │   Session Storage          │
│   LangGraph         │          │   (In-Memory / Redis)      │
│   Workflow          │          │                            │
│                     │          │   • Active Sessions        │
│  State Machine:     │          │   • Upload Metadata        │
│  1. Retrieve Docs   │          │   • Opportunities Cache    │
│  2. Grade Relevance │          │   • Workflow Results       │
│  3. Generate Answer │          └────────────────────────────┘
│  4. Check Quality   │
│  5. Architect Plan  │
│  6. Build Workflow  │
└─────┬───────────────┘
      │
      │ Uses
      │
┌─────▼──────────────────────────────────────────────────────┐
│                     RAG Pipeline                            │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   index.py   │  │ generator.py │  │  grader1.py  │     │
│  │              │  │              │  │              │     │
│  │ • Load Docs  │  │ • Prompt     │  │ • Document   │     │
│  │ • Split Text │  │ • LLM Call   │  │   Relevance  │     │
│  │ • Vectorize  │  │ • Generate   │  │ • Scoring    │     │
│  │ • Retrieve   │  │   Response   │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  grader2.py  │  │hallucinate   │  │answer_rewriter│    │
│  │              │  │_detector.py  │  │.py           │     │
│  │ • Answer     │  │              │  │              │     │
│  │   Quality    │  │ • Fact Check │  │ • Query      │     │
│  │ • Scoring    │  │ • Grounding  │  │   Transform  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────────────────────────────────────────┘
         │                            │
         │ Reads                      │ Indexes
         │                            │
┌────────▼──────────┐        ┌───────▼─────────────────────┐
│   Document Store  │        │   Vector Database (Chroma)  │
│                   │        │                             │
│   data/           │        │   • Embeddings              │
│   ├── pdf/        │        │   • Semantic Search         │
│   └── csv/        │        │   • Similarity Matching     │
└───────────────────┘        └─────────────────────────────┘
                                     │
                                     │ Queries
                                     │
                            ┌────────▼──────────┐
                            │ Google Gemini API │
                            │                   │
                            │   Model:          │
                            │   gemini-3-flash  │
                            │   -preview        │
                            └───────────────────┘
                                     │
                                     │ Interacts
                                     │
                            ┌────────▼──────────┐
                            │   n8n via MCP     │
                            │                   │
                            │   • Workflow API  │
                            │   • Node Catalog  │
                            │   • Deployment    │
                            └───────────────────┘
```

### Data Flow

1. **Upload Phase**: User uploads documents → FastAPI stores in `data/` → Returns session ID
2. **Analysis Phase**: `graph.py` loads docs → RAG pipeline analyzes → Extracts opportunities
3. **Selection Phase**: User selects opportunity → Frontend sends selection to API
4. **Generation Phase**: LangGraph architects workflow → MCP queries n8n docs → Generates JSON
5. **Deployment Phase**: Workflow JSON deployed to n8n or downloaded

---

## 📁 Project Structure

```
autoMate/
│
├── 🐍 Backend (Python)
│   ├── api_server.py              # FastAPI REST API server
│   ├── graph.py                   # Main LangGraph workflow orchestration
│   ├── main.py                    # Standalone CLI script
│   │
│   ├── RAG/                       # Retrieval-Augmented Generation Pipeline
│   │   ├── __init__.py
│   │   ├── index.py               # Document loading, splitting, vectorization
│   │   ├── generator.py           # LLM-based text generation
│   │   ├── grader1.py             # Document relevance assessment
│   │   ├── grader2.py             # Answer quality grading
│   │   ├── hallucinate_detector.py # Fact-checking and grounding
│   │   ├── answer_rewriter.py     # Query transformation
│   │   └── router.py              # Query routing logic
│   │
│   └── data/                      # Document storage (auto-created)
│       ├── pdf/                   # PDF uploads
│       └── csv/                   # CSV uploads
│
├── 🌐 Frontend (Next.js + TypeScript)
│   └── web/
│       ├── app/
│       │   ├── page.tsx           # Main application page
│       │   ├── layout.tsx         # Root layout with metadata
│       │   └── globals.css        # Global styles
│       │
│       ├── components/
│       │   ├── FileUploadZone.tsx       # Drag-and-drop uploader
│       │   ├── ProcessingView.tsx       # Analysis progress tracker
│       │   ├── OpportunitySelector.tsx  # Opportunity selection UI
│       │   └── ResultView.tsx           # Workflow result display
│       │
│       └── lib/
│           └── utils.ts           # Utility functions
│
├── 🔧 Configuration
│   ├── .env                       # Environment variables (SECRET - not in git)
│   ├── .env.example               # Environment template
│   ├── .gitignore                 # Git ignore rules
│   ├── pyproject.toml             # Python dependencies (uv)
│   ├── uv.lock                    # Locked Python dependencies
│   └── web/package.json           # Node.js dependencies
│
├── 🚀 Launcher Scripts
│   ├── start_api.ps1              # Launch API server only
│   └── start_fullstack.ps1        # Launch both API + Web UI
│
├── 📚 Documentation
│   ├── README.md                  # This file
│   └── INTEGRATION_GUIDE.md       # Detailed integration guide
│
└── 🔐 Security
    ├── .gitignore                 # Protects .env and data/
    └── .env.example               # Safe template for sharing
```

---

---

## 🔌 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 📤 `POST /api/analyze`

Analyzes uploaded documents and discovers automation opportunities.

**Request:**
```http
POST /api/analyze
Content-Type: multipart/form-data

files: File[]              # PDF or CSV files (max 10MB each)
context_url?: string       # Optional URL for additional context
question?: string          # Optional specific question to analyze
```

**Response:**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "opportunities": [
    {
      "id": "1",
      "title": "Automated Invoice Processing Workflow",
      "description": "Process invoices from email, extract data, update accounting system",
      "priority_score": 9,
      "department": "Finance",
      "estimated_time_savings": "15 hours/week",
      "complexity": "medium"
    },
    {
      "id": "2",
      "title": "Employee Onboarding Automation",
      "description": "Automate account creation, access provisioning, and welcome emails",
      "priority_score": 7,
      "department": "HR",
      "estimated_time_savings": "8 hours/week",
      "complexity": "low"
    }
  ],
  "analysis_stats": {
    "documents_processed": 3,
    "total_pages": 42,
    "processing_time": "12.3s",
    "opportunities_found": 5
  }
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid input (e.g., unsupported file type)
- `500` - Server error (e.g., LLM failure)

---

#### 🔨 `POST /api/build-workflow`

Generates n8n workflow JSON for a selected opportunity.

**Request:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "opportunity_index": 0
}
```

**Response:**
```json
{
  "success": true,
  "workflow": {
    "name": "Automated Invoice Processing",
    "nodes": [
      {
        "parameters": {
          "pollTimes": {
            "item": [
              {
                "mode": "everyMinute"
              }
            ]
          }
        },
        "name": "Email Trigger",
        "type": "n8n-nodes-base.emailReadImap",
        "position": [250, 300],
        "id": "node-1"
      },
      {
        "parameters": {
          "operation": "extractData"
        },
        "name": "Extract Invoice Data",
        "type": "n8n-nodes-base.code",
        "position": [450, 300],
        "id": "node-2"
      }
    ],
    "connections": {
      "Email Trigger": {
        "main": [[{"node": "Extract Invoice Data", "type": "main", "index": 0}]]
      }
    }
  },
  "deployment_url": "https://your-instance.app.n8n.cloud/workflow/123",
  "generation_time": "8.7s"
}
```

**Status Codes:**
- `200` - Success
- `404` - Session not found
- `500` - Generation failed

---

#### ❤️ `GET /api/health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "data_dir": "/path/to/data",
  "active_sessions": 3,
  "uptime": "2h 15m",
  "version": "1.0.0"
}
```

---

## 🛠️ Technology Stack

### Backend Infrastructure

| Technology | Purpose | Why We Chose It |
|-----------|---------|-----------------|
| **FastAPI** | REST API Framework | Modern, async, auto-documentation |
| **LangChain** | LLM Orchestration | Extensive integrations, robust |
| **LangGraph** | Workflow State Machine | Complex multi-step reasoning |
| **Google Gemini 3** | Cloud LLM Inference | Fast, reliable, cost-effective |
| **ChromaDB** | Vector Database | Efficient semantic search |
| **MCP** | n8n Protocol | Direct tool invocation |
| **Python 3.12** | Runtime | Latest features, performance |

### Frontend Stack

| Technology | Purpose | Why We Chose It |
|-----------|---------|-----------------|
| **Next.js 14** | React Framework | App Router, SSR, performance |
| **TypeScript** | Type Safety | Catch errors early, better DX |
| **Tailwind CSS** | Styling | Rapid development, consistency |
| **Framer Motion** | Animations | Smooth, declarative animations |
| **Lucide React** | Icons | Modern, tree-shakeable icons |

### AI & ML Components

| Component | Model/Service | Purpose |
|-----------|--------------|---------|
| **LLM** | Google Gemini 3 Flash | Text generation, reasoning |
| **Embeddings** | Chroma default | Document vectorization |
| **Vector Store** | ChromaDB | Semantic similarity search |
| **Tokenizer** | tiktoken | Token counting for chunking |

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### ❌ API Server Won't Start

**Symptoms:**
- Error: `ModuleNotFoundError: No module named 'fastapi'`
- Server crashes immediately

**Solutions:**
```powershell
# Reinstall dependencies
uv sync

# Verify installation
uv run python -c "import fastapi; print('OK')"

# Check Python version
python --version  # Should be 3.12+
```

---

#### ❌ Web UI Can't Connect to API

**Symptoms:**
- CORS errors in browser console
- "Failed to fetch" errors
- Connection refused

**Solutions:**

1. **Verify API is running:**
```powershell
curl http://localhost:8000/api/health
```

2. **Check firewall:**
```powershell
# Allow ports in Windows Firewall
New-NetFirewallRule -DisplayName "AutoMate API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

3. **Verify CORS settings** in `api_server.py`:
```python
allow_origins=["http://localhost:3000"]
```

---

#### ❌ Tiktoken Import Error

**Symptom:**
- Error: `Could not import tiktoken python package`

**Solution:**
```powershell
uv add tiktoken
# Then restart API server
```

---

#### ❌ Google Gemini API Error

**Symptoms:**
- Error: `Invalid API key` or `Authentication failed`
- Generation fails

**Solutions:**
```powershell
# Verify API key is set
echo $env:GOOGLE_API_KEY

# Test API connection
uv run python -c "from langchain_google_genai import ChatGoogleGenerativeAI; import os; from dotenv import load_dotenv; load_dotenv(); llm = ChatGoogleGenerativeAI(model='gemini-3-flash-preview', google_api_key=os.getenv('GOOGLE_API_KEY')); print(llm.invoke('Hello'))"

# Make sure key is in .env file
cat .env | Select-String "GOOGLE_API_KEY"
```

---

#### ❌ Empty Workflow Generation

**Symptoms:**
- Workflow JSON is incomplete
- Missing nodes or connections

**Solutions:**

1. **Check LLM output:**
```powershell
# Run in debug mode
cd C:\Users\amloul\Documents\autoMate
uv run python graph.py
```

2. **Verify n8n credentials:**
```env
N8N_API_KEY=your-actual-key-here
N8N_BASE_URL=https://your-instance.app.n8n.cloud
```

3. **Check MCP connection:**
- Ensure `npx` is available
- Test: `npx -y mcp-n8n`

---

#### ❌ File Upload Fails

**Symptoms:**
- "File too large" error
- Upload stuck at 0%

**Solutions:**

1. **Check file size:**
```powershell
# Max size is 10MB by default
# Edit api_server.py to increase:
File(..., max_length=20 * 1024 * 1024)  # 20MB
```

2. **Verify file format:**
- Only PDF and CSV are supported
- Ensure files aren't corrupted

3. **Check disk space:**
```powershell
Get-PSDrive C | Select-Object Used,Free
```

---

#### ❌ Port Already in Use

**Symptoms:**
- Error: `Address already in use`
- Server fails to bind to port

**Solutions:**

1. **Find process using port:**
```powershell
# For port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

2. **Use different port:**
```powershell
uvicorn api_server:api --port 8001
```

---

## 📚 Documentation

### Available Resources

- 📖 **[API Documentation](http://localhost:8000/docs)** - Interactive Swagger UI (when server running)
- 📘 **[Integration Guide](INTEGRATION_GUIDE.md)** - Detailed setup and integration walkthrough
- 🎓 **[n8n Docs](https://docs.n8n.io/)** - Understanding n8n workflows
- 🔗 **[LangChain Docs](https://python.langchain.com/)** - LLM orchestration patterns
- ⚛️ **[Next.js Docs](https://nextjs.org/docs)** - Frontend framework

### Getting Help

- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/automate-studio/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/automate-studio/discussions)
- 📧 **Contact**: your-email@example.com

---

## 🚀 Advanced Usage

### Running in Production

```powershell
# Build frontend
cd web
npm run build

# Run production server
npm start

# Run API with gunicorn (Linux/Mac)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_server:api
```

### Docker Deployment

```dockerfile
# Coming soon
# Dockerfile for containerized deployment
```

### Environment-Specific Configuration

```env
# Development
DEBUG=true
LOG_LEVEL=debug

# Production
DEBUG=false
LOG_LEVEL=info
ALLOWED_ORIGINS=https://yourdomain.com
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and commit: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Add tests for new features
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **n8n** - For the amazing workflow automation platform
- **LangChain** - For LLM orchestration tools
- **Google Gemini** - For powerful AI capabilities
- **Next.js Team** - For the incredible React framework
- **FastAPI** - For the modern Python web framework

---

## 🎓 Learn More

### Recommended Reading

- [RAG Fundamentals](https://python.langchain.com/docs/use_cases/question_answering/)
- [LangGraph Concepts](https://langchain-ai.github.io/langgraph/)
- [n8n Best Practices](https://docs.n8n.io/workflows/best-practices/)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ using AI and modern web technologies

[Report Bug](https://github.com/your-username/automate-studio/issues) • [Request Feature](https://github.com/your-username/automate-studio/issues) • [Documentation](INTEGRATION_GUIDE.md)

</div>
