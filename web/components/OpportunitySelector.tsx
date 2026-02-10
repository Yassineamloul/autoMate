'use client';

import { motion } from 'framer-motion';
import { Zap, ArrowLeft, TrendingUp, Building2 } from 'lucide-react';
import { cn } from '@/lib/utils';

type Opportunity = {
  id: string;
  title: string;
  priority_score: number;
  department?: string;
};

interface OpportunitySelectorProps {
  opportunities: Opportunity[];
  onSelect: (index: number) => void;
  onBack: () => void;
}

export default function OpportunitySelector({ opportunities, onSelect, onBack }: OpportunitySelectorProps) {
  // Sort by priority
  const sortedOpportunities = [...opportunities].sort(
    (a, b) => (b.priority_score || 0) - (a.priority_score || 0)
  );

  const getPriorityColor = (score: number) => {
    if (score >= 8) return 'text-green-400 bg-green-500/10 border-green-500/30';
    if (score >= 6) return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
    if (score >= 4) return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30';
    return 'text-zinc-400 bg-zinc-500/10 border-zinc-500/30';
  };

  const getPriorityLabel = (score: number) => {
    if (score >= 8) return 'High Priority';
    if (score >= 6) return 'Medium Priority';
    if (score >= 4) return 'Low Priority';
    return 'Consider';
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="max-w-4xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-8">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", duration: 0.6 }}
          className="inline-block p-4 bg-blue-500/20 rounded-full mb-4"
        >
          <Zap className="w-12 h-12 text-blue-500" />
        </motion.div>
        
        <h2 className="text-3xl font-bold text-zinc-100 mb-2">
          Automation Opportunities Found
        </h2>
        <p className="text-zinc-400">
          Select which workflow you'd like to build
        </p>
      </div>

      {/* Opportunities List */}
      <div className="space-y-4 mb-8">
        {sortedOpportunities.map((opp, index) => (
          <motion.button
            key={opp.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02, x: 4 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelect(index)}
            className="w-full glass glass-hover p-6 rounded-xl text-left group transition-all"
          >
            <div className="flex items-start gap-4">
              {/* Rank Badge */}
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg">
                  {index + 1}
                </div>
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-semibold text-zinc-100 mb-2 group-hover:text-blue-400 transition-colors">
                  {opp.title}
                </h3>
                
                <div className="flex items-center gap-3 flex-wrap">
                  {/* Priority Badge */}
                  <span className={cn(
                    "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border",
                    getPriorityColor(opp.priority_score)
                  )}>
                    <TrendingUp className="w-3 h-3" />
                    {getPriorityLabel(opp.priority_score)}
                  </span>

                  {/* Priority Score */}
                  <span className="text-sm text-zinc-500">
                    Score: <span className="text-zinc-300 font-medium">{opp.priority_score}/10</span>
                  </span>

                  {/* Department */}
                  {opp.department && (
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-zinc-800 text-zinc-300 border border-zinc-700">
                      <Building2 className="w-3 h-3" />
                      {opp.department}
                    </span>
                  )}
                </div>
              </div>

              {/* Arrow */}
              <div className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center">
                  <svg className="w-4 h-4 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          </motion.button>
        ))}
      </div>

      {/* Back Button */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onBack}
        className="w-full text-zinc-400 hover:text-zinc-200 font-medium py-3 px-6 rounded-xl border border-zinc-800 hover:border-zinc-700 transition-colors"
      >
        <span className="flex items-center justify-center gap-2">
          <ArrowLeft className="w-4 h-4" />
          Start Over
        </span>
      </motion.button>
    </motion.div>
  );
}
