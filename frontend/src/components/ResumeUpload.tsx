'use client';

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { uploadResume, calculateMatch } from '@/lib/api';
import type { MatchData } from '@/types';

interface ResumeUploadProps {
  onMatchComplete: (data: MatchData) => void;
}

export default function ResumeUpload({ onMatchComplete }: ResumeUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resumeText, setResumeText] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError('');
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please upload a resume');
      return;
    }
    
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Step 1: Upload and parse resume
      const resumeData = await uploadResume(file);
      setResumeText(resumeData.extracted_text);

      // Step 2: Calculate match
      const matchData = await calculateMatch(
        resumeData.extracted_text,
        jobDescription,
        jobTitle || 'Target Role'
      );

      onMatchComplete(matchData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process resume. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto"
    >
      {/* Hero Section */}
      <div className="text-center mb-12">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-5xl font-bold text-white mb-4"
        >
          From Resume to Role, <span className="text-indigo-400">Intelligently</span>
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-xl text-gray-300 max-w-2xl mx-auto"
        >
          Upload your resume and discover your perfect career fit with AI-powered semantic matching
        </motion.p>
      </div>

      {/* Upload Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-slate-800/50 backdrop-blur-sm border border-indigo-800/30 rounded-xl p-8 shadow-2xl"
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Upload Resume (PDF or DOCX)
            </label>
            <div
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              className="border-2 border-dashed border-indigo-600/50 rounded-lg p-8 text-center hover:border-indigo-500 transition-colors cursor-pointer bg-slate-900/30"
            >
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                {file ? (
                  <div className="flex items-center justify-center gap-2 text-indigo-400">
                    <FileText className="w-6 h-6" />
                    <span>{file.name}</span>
                  </div>
                ) : (
                  <div>
                    <Upload className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-300">
                      Drop your resume here or <span className="text-indigo-400">browse</span>
                    </p>
                    <p className="text-sm text-gray-500 mt-1">PDF or DOCX, max 10MB</p>
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* Job Title */}
          <div>
            <label htmlFor="job-title" className="block text-sm font-medium text-gray-200 mb-2">
              Target Job Title (Optional)
            </label>
            <input
              type="text"
              id="job-title"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              placeholder="e.g., Machine Learning Engineer"
              className="w-full px-4 py-3 bg-slate-900/50 border border-indigo-800/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>

          {/* Job Description */}
          <div>
            <label htmlFor="job-description" className="block text-sm font-medium text-gray-200 mb-2">
              Job Description
            </label>
            <textarea
              id="job-description"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              rows={8}
              className="w-full px-4 py-3 bg-slate-900/50 border border-indigo-800/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-400 text-sm">
              {error}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:cursor-not-allowed text-white font-medium py-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Target className="w-5 h-5" />
                Analyze Match
              </>
            )}
          </button>
        </form>
      </motion.div>

      {/* Features */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12"
      >
        {[
          { icon: '🎯', title: 'Semantic Matching', desc: 'Goes beyond keywords' },
          { icon: '📊', title: 'Skill Heatmap', desc: 'Visualize your gaps' },
          { icon: '🚀', title: 'Learning Roadmap', desc: 'Personalized plan' },
        ].map((feature, idx) => (
          <div
            key={idx}
            className="bg-slate-800/30 border border-indigo-800/20 rounded-lg p-6 text-center"
          >
            <div className="text-4xl mb-2">{feature.icon}</div>
            <h3 className="text-white font-semibold mb-1">{feature.title}</h3>
            <p className="text-gray-400 text-sm">{feature.desc}</p>
          </div>
        ))}
      </motion.div>
    </motion.div>
  );
}
