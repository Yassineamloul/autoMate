# Changelog

All notable changes to AutoMate Studio will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-10

### 🎉 Initial Release

#### Added
- **RAG-Based Document Analysis**: Intelligent document processing using LangChain and ChromaDB
- **Automation Discovery**: AI identifies automation opportunities from business documents
- **Priority Scoring**: Opportunities ranked by impact and feasibility (1-10 scale)
- **Interactive Workflow Builder**: Generate n8n workflows from selected opportunities
- **Modern Web UI**: Next.js 14 with Tailwind CSS and glassmorphism design
- **FastAPI Backend**: Async Python server with REST API
- **Real-Time Progress**: Live updates during analysis and generation
- **n8n Integration**: Direct deployment via MCP protocol
- **Multi-Document Support**: Upload multiple PDFs and CSVs
- **Context URL Support**: Additional context from web pages
- **Session Management**: Persistent session state across requests
- **Health Check Endpoint**: `/api/health` for monitoring
- **Environment Configuration**: Secure API key management via `.env`

#### Features
- Document upload with drag-and-drop
- PDF and CSV parsing
- Vector similarity search
- LLM-powered opportunity extraction
- Workflow JSON generation
- Direct n8n deployment
- Download workflow JSON
- Responsive design
- Dark mode UI
- Smooth animations

#### Technology Stack
- Python 3.12+
- FastAPI
- LangChain
- LangGraph
- Ollama (gpt-oss:120b-cloud)
- ChromaDB
- Next.js 14
- TypeScript
- Tailwind CSS
- Framer Motion

#### Documentation
- Comprehensive README.md
- API documentation (Swagger UI)
- Integration guide
- Installation instructions
- Troubleshooting guide

#### Security
- API keys stored in `.env`
- CORS protection
- Input validation
- File size limits
- Secure file storage

---

## [Unreleased]

### Planned Features
- [ ] Docker containerization
- [ ] Database persistence (PostgreSQL)
- [ ] User authentication
- [ ] Multi-user support
- [ ] Workflow history
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Scheduled analysis
- [ ] Webhook support
- [ ] Custom LLM models
- [ ] Advanced filtering
- [ ] Export to other platforms (Make.com, Zapier)

---

## Release Notes Format

### Types of Changes
- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements

---

[1.0.0]: https://github.com/your-username/automate-studio/releases/tag/v1.0.0
