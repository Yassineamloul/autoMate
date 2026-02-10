# AutoMate - Complete Integration Guide

## 🎉 What's New

Your AutoMate Studio now has **full Python integration**! The web UI connects directly to your `graph.py` workflow.

### Key Features

✅ **File Management**: Uploads are stored in `data/` folder (previous files are automatically cleaned)  
✅ **Real-Time Processing**: Uses your actual RAG pipeline and AI agents  
✅ **Opportunity Selection**: Choose which automation scenario to build from the UI  
✅ **Live Workflow Generation**: Your Python code generates the n8n workflow  

---

## 🚀 Quick Start

### 1. Install Backend Dependencies

```powershell
# In the main autoMate folder
uv sync
```

This will install FastAPI, uvicorn, and other required packages.

### 2. Start the API Server

```powershell
# Make sure your virtual environment is activated
.\.venv\Scripts\activate.ps1

# Start the FastAPI server
python api_server.py
```

The API will run on **http://localhost:8000**

### 3. Start the Frontend

Open a **new terminal** and run:

```powershell
cd web
npm run dev
```

The web UI will be at **http://localhost:3000**

---

## 📋 How It Works

### Step 1: Upload & Analyze
1. User uploads PDF/CSV files via the web UI
2. Files are saved to `data/` folder (old files deleted)
3. Backend runs the RAG phase from `graph.py`
4. AI analyzes documents and finds automation opportunities

### Step 2: Choose Automation
1. UI displays all opportunities found (sorted by priority)
2. User selects which automation to build
3. Backend continues with the planner and executor phases

### Step 3: Generate Workflow
1. AI designs the workflow architecture
2. Generates n8n-compatible JSON
3. User can download or deploy to n8n

---

## 🔧 API Endpoints

### `POST /api/analyze`
Uploads files and finds automation opportunities
- **Body**: FormData with files, optional context_url
- **Returns**: List of opportunities + session_id

### `POST /api/build-workflow`
Builds workflow for selected opportunity
- **Body**: `{ "session_id": "...", "opportunity_index": 0 }`
- **Returns**: Generated workflow JSON

### `GET /api/health`
Check API status

---

## 📁 File Structure

```
autoMate/
├── api_server.py          # FastAPI backend (NEW)
├── graph.py               # Your RAG + Builder workflow
├── data/                  # Upload directory (auto-managed)
│   ├── pdf/
│   └── csv/
├── web/                   # Next.js frontend
│   ├── app/
│   │   └── page.tsx       # Updated with API integration
│   └── components/
│       ├── OpportunitySelector.tsx  # NEW component
│       └── ...
└── workflow_final.json    # Generated output
```

---

## 🐛 Troubleshooting

### "Connection refused" errors
- Make sure the API server is running on port 8000
- Check that `.venv` is activated when running `api_server.py`

### "No opportunities found"
- Ensure your documents are in `.pdf` or `.csv` format
- Check that your RAG pipeline has indexed documents
- Look at the terminal logs for detailed error messages

### Empty workflow JSON
- This is the issue you mentioned in `graph.py`
- The API will help debug this by showing exactly what the planner returns
- Check the `parse_output` node is extracting opportunities correctly

---

## 🔄 Running Both Servers

Use two terminal windows:

**Terminal 1 - API Server:**
```powershell
.\.venv\Scripts\activate.ps1
python api_server.py
```

**Terminal 2 - Web UI:**
```powershell
cd web
npm run dev
```

---

## 📊 Testing the Integration

1. Visit http://localhost:3000
2. Upload a test PDF or CSV file
3. Click "Analyze & Find Opportunities"
4. You should see real opportunities from your RAG analysis
5. Select one and click to build
6. Download the generated workflow JSON

---

## 🎯 Next Steps

1. **Fix the empty workflow issue**: Debug why `nodes` and `connections` are empty
2. **Add real-time logs**: Stream Python logs to the UI using WebSockets
3. **Deploy**: Host the API and frontend for production use

---

## 💡 Pro Tips

- The API stores sessions in memory (use Redis for production)
- File uploads are limited to PDF and CSV (modify `api_server.py` to add more)
- The `data/` folder is cleaned on each new upload
- Check http://localhost:8000/docs for interactive API documentation

---

Happy Automating! 🚀
