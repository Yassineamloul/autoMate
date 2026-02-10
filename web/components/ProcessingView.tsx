'use client';

import { motion } from 'framer-motion';
import { CheckCircle2, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

type ProcessingStep = {
  id: string;
  label: string;
  status: 'pending' | 'active' | 'completed';
};

interface ProcessingViewProps {
  steps: ProcessingStep[];
  logs: string[];
}

export default function ProcessingView({ steps, logs }: ProcessingViewProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="max-w-5xl mx-auto space-y-8"
    >
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-zinc-100 mb-2">
          Processing Your Workflow
        </h2>
        <p className="text-zinc-400">
          Our AI is analyzing your documents and creating the perfect automation
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Step Visualizer */}
        <div className="glass p-8 rounded-2xl">
          <h3 className="text-lg font-semibold text-zinc-100 mb-6">Progress</h3>
          <div className="space-y-6">
            {steps.map((step, index) => (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-4"
              >
                {/* Status Icon */}
                <div className={cn(
                  "flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all",
                  step.status === 'completed' && "bg-green-500/20 border-green-500",
                  step.status === 'active' && "bg-blue-500/20 border-blue-500",
                  step.status === 'pending' && "bg-zinc-800 border-zinc-700"
                )}>
                  {step.status === 'completed' && (
                    <CheckCircle2 className="w-5 h-5 text-green-500" />
                  )}
                  {step.status === 'active' && (
                    <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
                  )}
                  {step.status === 'pending' && (
                    <div className="w-2 h-2 rounded-full bg-zinc-600" />
                  )}
                </div>

                {/* Step Label */}
                <div className="flex-1">
                  <p className={cn(
                    "font-medium transition-colors",
                    step.status === 'completed' && "text-green-400",
                    step.status === 'active' && "text-blue-400",
                    step.status === 'pending' && "text-zinc-500"
                  )}>
                    {step.label}
                  </p>
                </div>

                {/* Pulsing dots for active step */}
                {step.status === 'active' && (
                  <div className="flex gap-1">
                    {[0, 1, 2].map((i) => (
                      <motion.div
                        key={i}
                        className="w-2 h-2 rounded-full bg-blue-500"
                        animate={{ opacity: [0.3, 1, 0.3] }}
                        transition={{
                          duration: 1.5,
                          repeat: Infinity,
                          delay: i * 0.2
                        }}
                      />
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>

        {/* Terminal Log */}
        <div className="glass p-8 rounded-2xl">
          <h3 className="text-lg font-semibold text-zinc-100 mb-6">Live Log</h3>
          <div className="bg-black/50 rounded-lg p-4 h-[400px] overflow-y-auto terminal">
            <div className="space-y-2">
              {logs.map((log, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-sm text-green-400 font-mono"
                >
                  {log}
                </motion.div>
              ))}
              {logs.length > 0 && (
                <motion.div
                  animate={{ opacity: [1, 0] }}
                  transition={{ duration: 0.8, repeat: Infinity }}
                  className="inline-block w-2 h-4 bg-green-400 ml-1"
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
