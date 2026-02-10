'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, Download, ExternalLink, RefreshCw, Loader2 } from 'lucide-react';

interface ResultViewProps {
  workflowData: any;
  selectedOpportunity: any;
  n8nUrl: string;
  onDownload: () => void;
  onReset: () => void;
}

export default function ResultView({ workflowData, selectedOpportunity, n8nUrl, onDownload, onReset }: ResultViewProps) {
  const [isDeploying, setIsDeploying] = useState(false);
  const [isDeployed, setIsDeployed] = useState(false);

  const handleDeploy = async () => {
    setIsDeploying(true);
    // Simulate deployment
    await new Promise(resolve => setTimeout(resolve, 2000));
    setIsDeploying(false);
    setIsDeployed(true);
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="max-w-3xl mx-auto"
    >
      {/* Success Card */}
      <div className="glass p-8 rounded-2xl mb-8">
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", duration: 0.6 }}
            className="inline-block p-4 bg-green-500/20 rounded-full mb-4"
          >
            <CheckCircle2 className="w-16 h-16 text-green-500" />
          </motion.div>
          
          <h2 className="text-3xl font-bold text-zinc-100 mb-2">
            Workflow Generated Successfully!
          </h2>
          <p className="text-zinc-400">
            Your automation is ready to use
          </p>
        </div>

        {/* Opportunity Summary */}
        <div className="bg-zinc-900/50 rounded-xl p-6 mb-6">
          <h3 className="text-sm font-medium text-zinc-400 mb-2">
            Selected Automation
          </h3>
          <p className="text-xl font-semibold text-zinc-100">
            {selectedOpportunity?.title || workflowData?.name || 'Workflow Generated'}
          </p>
          
          <div className="mt-4 flex items-center gap-4 text-sm text-zinc-400">
            {selectedOpportunity?.priority_score && (
              <div>
                <span className="text-zinc-500">Priority Score:</span>{' '}
                <span className="text-zinc-200 font-medium">
                  {selectedOpportunity.priority_score}/10
                </span>
              </div>
            )}
            {selectedOpportunity?.department && (
              <div>
                <span className="text-zinc-500">Department:</span>{' '}
                <span className="text-zinc-200 font-medium">
                  {selectedOpportunity.department}
                </span>
              </div>
            )}
            <div>
              <span className="text-zinc-500">Nodes:</span>{' '}
              <span className="text-zinc-200 font-medium">
                {workflowData?.nodes?.length || 0}
              </span>
            </div>
            <div>
              <span className="text-zinc-500">Connections:</span>{' '}
              <span className="text-zinc-200 font-medium">
                {Object.keys(workflowData?.connections || {}).length}
              </span>
            </div>
          </div>
        </div>

        {/* Action Area */}
        <div className="space-y-4">
          {n8nUrl ? (
            // If n8n URL provided
            <div className="space-y-3">
              {!isDeployed ? (
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleDeploy}
                  disabled={isDeploying}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-zinc-700 disabled:to-zinc-700 text-white font-semibold py-4 px-6 rounded-xl shadow-lg transition-all"
                >
                  {isDeploying ? (
                    <span className="flex items-center justify-center gap-2">
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Deploying to n8n...
                    </span>
                  ) : (
                    <span className="flex items-center justify-center gap-2">
                      <ExternalLink className="w-5 h-5" />
                      Deploy to n8n
                    </span>
                  )}
                </motion.button>
              ) : (
                <motion.a
                  href={n8nUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  whileHover={{ scale: 1.02 }}
                  className="block w-full bg-green-600 hover:bg-green-500 text-white font-semibold py-4 px-6 rounded-xl shadow-lg transition-all text-center"
                >
                  <span className="flex items-center justify-center gap-2">
                    <CheckCircle2 className="w-5 h-5" />
                    Open in n8n
                  </span>
                </motion.a>
              )}
              
              <button
                onClick={onDownload}
                className="w-full bg-zinc-800 hover:bg-zinc-700 text-zinc-100 font-medium py-3 px-6 rounded-xl transition-colors"
              >
                <span className="flex items-center justify-center gap-2">
                  <Download className="w-4 h-4" />
                  Download JSON
                </span>
              </button>
            </div>
          ) : (
            // If no n8n URL - auto download
            <div className="space-y-3">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={onDownload}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold py-4 px-6 rounded-xl shadow-lg transition-all"
              >
                <span className="flex items-center justify-center gap-2">
                  <Download className="w-5 h-5" />
                  Download Workflow JSON
                </span>
              </motion.button>
              
              <p className="text-center text-sm text-zinc-500">
                Import this file into your n8n instance manually
              </p>
            </div>
          )}

          {/* Reset Button */}
          <button
            onClick={onReset}
            className="w-full mt-6 text-zinc-400 hover:text-zinc-200 font-medium py-3 px-6 rounded-xl border border-zinc-800 hover:border-zinc-700 transition-colors"
          >
            <span className="flex items-center justify-center gap-2">
              <RefreshCw className="w-4 h-4" />
              Create Another Workflow
            </span>
          </button>
        </div>
      </div>

      {/* Workflow Preview (Optional) */}
      <div className="glass p-6 rounded-2xl">
        <h3 className="text-lg font-semibold text-zinc-100 mb-4">
          Workflow Preview
        </h3>
        <div className="bg-zinc-900/50 rounded-lg p-4 max-h-[300px] overflow-auto">
          <pre className="text-xs text-zinc-400 font-mono">
            {JSON.stringify(workflowData, null, 2)}
          </pre>
        </div>
      </div>
    </motion.div>
  );
}
