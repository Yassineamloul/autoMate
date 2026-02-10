'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Link as LinkIcon, Sparkles, Download, ExternalLink, CheckCircle2, Loader2 } from 'lucide-react';
import FileUploadZone from '@/components/FileUploadZone';
import ProcessingView from '@/components/ProcessingView';
import OpportunitySelector from '@/components/OpportunitySelector';
import ResultView from '@/components/ResultView';

type ProcessingStep = {
  id: string;
  label: string;
  status: 'pending' | 'active' | 'completed';
};

type Opportunity = {
  id: string;
  title: string;
  priority_score: number;
  department?: string;
};

type ViewState = 'input' | 'analyzing' | 'selecting' | 'building' | 'complete';

const API_BASE_URL = 'http://localhost:8000';

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [contextUrl, setContextUrl] = useState('');
  const [n8nUrl, setN8nUrl] = useState('');
  const [viewState, setViewState] = useState<ViewState>('input');
  const [steps, setSteps] = useState<ProcessingStep[]>([
    { id: '1', label: 'Analyzing Documents', status: 'pending' },
    { id: '2', label: 'Finding Automation Opportunities', status: 'pending' },
    { id: '3', label: 'Architecting Workflow', status: 'pending' },
    { id: '4', label: 'Writing Code', status: 'pending' },
  ]);
  const [logs, setLogs] = useState<string[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [sessionId, setSessionId] = useState<string>('');
  const [workflowData, setWorkflowData] = useState<any>(null);
  const [selectedOpportunity, setSelectedOpportunity] = useState<Opportunity | null>(null);

  const handleAnalyze = async () => {
    if (files.length === 0) {
      alert('Please upload at least one file');
      return;
    }

    setViewState('analyzing');
    setLogs([]);
    setSteps(steps.map(s => ({ ...s, status: 'pending' as const })));

    try {
      // Step 1: Analyzing Documents
      setSteps(prev => prev.map((step, idx) => ({
        ...step,
        status: idx === 0 ? 'active' : 'pending'
      })));
      setLogs(prev => [...prev, `> Uploading ${files.length} file(s)...`]);

      const formData = new FormData();
      files.forEach(file => formData.append('files', file));
      if (contextUrl) formData.append('context_url', contextUrl);

      const response = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error Response:', errorText);
        throw new Error(`Analysis failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      
      setLogs(prev => [...prev, '> Files uploaded successfully']);
      setLogs(prev => [...prev, '> Extracting content...']);
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Step 2: Finding Opportunities
      setSteps(prev => prev.map((step, idx) => ({
        ...step,
        status: idx === 0 ? 'completed' : idx === 1 ? 'active' : 'pending'
      })));
      
      setLogs(prev => [...prev, '> Analyzing document structure...']);
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setLogs(prev => [...prev, `> Found ${data.opportunities.length} automation opportunities!`]);
      
      setSteps(prev => prev.map((step, idx) => ({
        ...step,
        status: idx <= 1 ? 'completed' : 'pending'
      })));

      // Store session and opportunities
      setSessionId(data.session_id);
      setOpportunities(data.opportunities);
      
      // Move to opportunity selection
      await new Promise(resolve => setTimeout(resolve, 1000));
      setViewState('selecting');

    } catch (error) {
      console.error('Error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      alert(`Failed to analyze documents: ${errorMessage}\n\nCheck the browser console (F12) for details.`);
      setViewState('input');
    }
  };

  const handleOpportunitySelect = async (index: number) => {
    const selected = opportunities[index];
    setSelectedOpportunity(selected);
    setViewState('building');
    
    try {
      // Step 3: Architecting Workflow
      setSteps(prev => prev.map((step, idx) => ({
        ...step,
        status: idx <= 1 ? 'completed' : idx === 2 ? 'active' : 'pending'
      })));
      
      setLogs([
        ...logs,
        `> Selected: ${selected.title}`,
        '> Analyzing automation requirements...',
        '> Designing workflow architecture...'
      ]);

      await new Promise(resolve => setTimeout(resolve, 2000));

      // Step 4: Building Workflow
      setSteps(prev => prev.map((step, idx) => ({
        ...step,
        status: idx <= 2 ? 'completed' : idx === 3 ? 'active' : 'pending'
      })));
      
      setLogs(prev => [
        ...prev,
        '> Creating n8n nodes...',
        '> Configuring node connections...',
        '> Generating workflow JSON...'
      ]);

      const response = await fetch(`${API_BASE_URL}/api/build-workflow`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          opportunity_index: index
        })
      });

      if (!response.ok) {
        throw new Error('Workflow build failed');
      }

      const data = await response.json();
      
      setLogs(prev => [...prev, '> Workflow generation complete!']);
      setSteps(prev => prev.map(step => ({ ...step, status: 'completed' as const })));
      
      setWorkflowData(data.workflow);
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      setViewState('complete');

    } catch (error) {
      console.error('Error:', error);
      alert('Failed to build workflow. Check console for details.');
      setViewState('selecting');
    }
  };

  const handleReset = () => {
    setFiles([]);
    setContextUrl('');
    setN8nUrl('');
    setViewState('input');
    setSteps(steps.map(s => ({ ...s, status: 'pending' as const })));
    setLogs([]);
    setWorkflowData(null);
    setOpportunities([]);
    setSessionId('');
    setSelectedOpportunity(null);
  };

  const handleDownload = async () => {
    if (!workflowData) return;
    
    const dataStr = JSON.stringify(workflowData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = 'workflow.json';
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-zinc-950 via-zinc-900 to-zinc-950">
      {/* Animated background gradient */}
      <div className="fixed inset-0 bg-gradient-to-br from-blue-500/10 via-purple-500/10 to-pink-500/10 animate-pulse" />
      
      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="w-10 h-10 text-blue-500" />
            <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
              AutoMate
            </h1>
          </div>
          <p className="text-xl text-zinc-400">
            Turn your documents into n8n workflows instantly
          </p>
        </motion.div>

        <AnimatePresence mode="wait">
          {viewState === 'input' ? (
            // Input Section
            <motion.div
              key="input"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="max-w-4xl mx-auto space-y-8"
            >
              {/* File Upload */}
              <FileUploadZone files={files} setFiles={setFiles} />

              {/* Context URL */}
              <div className="glass p-6 rounded-2xl">
                <label className="flex items-center gap-2 text-sm font-medium mb-3 text-zinc-300">
                  <LinkIcon className="w-4 h-4" />
                  Context URL (Optional)
                </label>
                <input
                  type="url"
                  value={contextUrl}
                  onChange={(e) => setContextUrl(e.target.value)}
                  placeholder="https://docs.example.com/api"
                  className="w-full bg-zinc-900/50 border border-zinc-800 rounded-lg px-4 py-3 text-zinc-100 placeholder-zinc-500 focus:border-blue-500 focus:outline-none transition-colors"
                />
              </div>

              {/* n8n Configuration */}
              <div className="glass p-6 rounded-2xl">
                <label className="flex items-center gap-2 text-sm font-medium mb-3 text-zinc-300">
                  <ExternalLink className="w-4 h-4" />
                  n8n Instance URL (Optional)
                  <span className="ml-auto text-xs text-zinc-500">
                    Leave empty to download JSON manually
                  </span>
                </label>
                <input
                  type="url"
                  value={n8nUrl}
                  onChange={(e) => setN8nUrl(e.target.value)}
                  placeholder="https://your-n8n-instance.com"
                  className="w-full bg-zinc-900/50 border border-zinc-800 rounded-lg px-4 py-3 text-zinc-100 placeholder-zinc-500 focus:border-blue-500 focus:outline-none transition-colors"
                />
              </div>

              {/* Analyze Button */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleAnalyze}
                disabled={files.length === 0}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-zinc-800 disabled:to-zinc-800 disabled:cursor-not-allowed text-white font-semibold py-4 px-8 rounded-xl text-lg shadow-lg shadow-blue-500/25 transition-all"
              >
                <span className="flex items-center justify-center gap-2">
                  <Sparkles className="w-5 h-5" />
                  Analyze & Find Opportunities
                </span>
              </motion.button>
            </motion.div>
          ) : viewState === 'analyzing' || viewState === 'building' ? (
            // Processing View
            <ProcessingView steps={steps} logs={logs} />
          ) : viewState === 'selecting' ? (
            // Opportunity Selection
            <OpportunitySelector 
              opportunities={opportunities}
              onSelect={handleOpportunitySelect}
              onBack={handleReset}
            />
          ) : (
            // Result View
            <ResultView
              workflowData={workflowData}
              selectedOpportunity={selectedOpportunity}
              n8nUrl={n8nUrl}
              onDownload={handleDownload}
              onReset={handleReset}
            />
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
