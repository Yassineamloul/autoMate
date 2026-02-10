# AutoMate Studio - Web UI

A modern, beautiful web interface for the AutoMate project - turning documents into n8n workflows instantly.

## 🎨 Features

- **Glassmorphism UI**: Modern, clean design with dark mode
- **Drag & Drop**: Easy file upload for PDF and CSV files
- **Live Processing**: Real-time visualization of AI workflow generation
- **Opportunity Selection**: Choose which automation scenario to build
- **Terminal Log**: Matrix-style live log showing processing steps
- **n8n Integration**: Direct deployment to n8n or JSON download
- **Framer Motion Animations**: Smooth, professional transitions

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- **API Server running** (see main README)

### Installation

```bash
cd web
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

**Important**: The web UI requires the FastAPI backend to be running on `http://localhost:8000`. Start the API first using `.\start_api.ps1` from the main directory.

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React

## 📁 Project Structure

```
web/
├── app/
│   ├── globals.css      # Global styles + glassmorphism
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Main application page
├── components/
│   ├── FileUploadZone.tsx       # Drag & drop file upload
│   ├── ProcessingView.tsx       # Live processing visualization
│   ├── OpportunitySelector.tsx  # Automation opportunity picker
│   └── ResultView.tsx           # Success screen & download
└── lib/
    └── utils.ts         # Utility functions
```

## 🔌 Backend Integration

The UI connects to the Python FastAPI backend:

- `POST /api/analyze` - Upload files and get automation opportunities
- `POST /api/build-workflow` - Build workflow for selected opportunity
- `GET /api/download-workflow` - Download generated workflow JSON

API base URL is configured in `app/page.tsx` as `http://localhost:8000`.

## 🎨 Customization

### Colors

Edit the color scheme in `tailwind.config.js` and `app/globals.css`.

### Animations

Modify Framer Motion animations in the component files.

## 📦 Build for Production

```bash
npm run build
npm start
```

## 🐛 Known Issues

- Requires backend API to be running on port 8000
- CORS is enabled for `localhost:3000` only

## 📄 License

Part of the AutoMate project.
