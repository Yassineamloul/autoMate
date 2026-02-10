'use client';

import { useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface FileUploadZoneProps {
  files: File[];
  setFiles: (files: File[]) => void;
}

export default function FileUploadZone({ files, setFiles }: FileUploadZoneProps) {
  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const droppedFiles = Array.from(e.dataTransfer.files).filter(
      file => file.type === 'application/pdf' || file.type === 'text/csv'
    );
    setFiles([...files, ...droppedFiles]);
  }, [files, setFiles]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files).filter(
        file => file.type === 'application/pdf' || file.type === 'text/csv'
      );
      setFiles([...files, ...selectedFiles]);
    }
  }, [files, setFiles]);

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <motion.div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        whileHover={{ scale: 1.01 }}
        className={cn(
          "glass glass-hover relative border-2 border-dashed border-zinc-700 rounded-2xl p-12 text-center cursor-pointer transition-all",
          files.length > 0 && "border-blue-500/50"
        )}
      >
        <input
          type="file"
          multiple
          accept=".pdf,.csv"
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        <div className="flex flex-col items-center gap-4">
          <motion.div
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="p-4 bg-blue-500/10 rounded-full"
          >
            <Upload className="w-12 h-12 text-blue-500" />
          </motion.div>
          
          <div>
            <h3 className="text-xl font-semibold text-zinc-100 mb-2">
              Drop your files here
            </h3>
            <p className="text-zinc-400 text-sm">
              Or click to browse • Supports PDF and CSV files
            </p>
          </div>
        </div>
      </motion.div>

      {/* File List */}
      {files.length > 0 && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="space-y-2"
        >
          {files.map((file, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="glass p-4 rounded-lg flex items-center justify-between group"
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                  <FileText className="w-5 h-5 text-blue-500" />
                </div>
                <div>
                  <p className="text-sm font-medium text-zinc-100">{file.name}</p>
                  <p className="text-xs text-zinc-500">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              </div>
              
              <button
                onClick={() => removeFile(index)}
                className="p-2 hover:bg-red-500/10 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
              >
                <X className="w-4 h-4 text-red-500" />
              </button>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}
