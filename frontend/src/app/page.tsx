'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Target, TrendingUp, Sparkles } from 'lucide-react';
import ResumeUpload from '@/components/ResumeUpload';
import MatchResults from '@/components/MatchResults';
import SkillHeatmap from '@/components/SkillHeatmap';
import LearningRoadmap from '@/components/LearningRoadmap';
import type { MatchData, RoadmapData, CourseRecommendation, AlternativeCareer } from '@/types';

export default function Home() {
  const [step, setStep] = useState<'upload' | 'results' | 'roadmap'>('upload');
  const [matchData, setMatchData] = useState<MatchData | null>(null);
  const [roadmapData, setRoadmapData] = useState<RoadmapData | null>(null);
  const [recommendations, setRecommendations] = useState<CourseRecommendation[]>([]);
  const [alternatives, setAlternatives] = useState<AlternativeCareer[]>([]);

  const handleMatchComplete = (data: MatchData) => {
    setMatchData(data);
    setStep('results');
  };

  const handleGenerateRoadmap = (
    roadmap: RoadmapData,
    recs: CourseRecommendation[],
    alt: AlternativeCareer[]
  ) => {
    setRoadmapData(roadmap);
    setRecommendations(recs);
    setAlternatives(alt);
    setStep('roadmap');
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900">
      {/* Header */}
      <header className="border-b border-indigo-800/30 backdrop-blur-sm bg-slate-900/50">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-2"
            >
              <Sparkles className="w-8 h-8 text-indigo-400" />
              <h1 className="text-2xl font-bold text-white">Career Path Optimizer</h1>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-4 text-sm text-gray-300"
            >
              <button
                type="button"
                onClick={() => setStep('upload')}
                className={`flex items-center gap-2 rounded-lg px-3 py-2 transition-colors ${
                  step === 'upload'
                    ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40'
                    : 'text-gray-400 hover:text-gray-200'
                }`}
              >
                <Upload className="w-4 h-4" />
                <span className="font-medium">Upload</span>
              </button>
              <button
                type="button"
                onClick={() => setStep('results')}
                disabled={!matchData}
                className={`flex items-center gap-2 rounded-lg px-3 py-2 transition-colors ${
                  step === 'results'
                    ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40'
                    : 'text-gray-400 hover:text-gray-200'
                } ${!matchData ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <Target className="w-4 h-4" />
                <span className="font-medium">Analysis</span>
              </button>
              <button
                type="button"
                onClick={() => setStep('roadmap')}
                disabled={!roadmapData}
                className={`flex items-center gap-2 rounded-lg px-3 py-2 transition-colors ${
                  step === 'roadmap'
                    ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40'
                    : 'text-gray-400 hover:text-gray-200'
                } ${!roadmapData ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <TrendingUp className="w-4 h-4" />
                <span className="font-medium">Roadmap</span>
              </button>
            </motion.div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        {step === 'upload' && (
          <ResumeUpload onMatchComplete={handleMatchComplete} />
        )}
        
        {step === 'results' && matchData && (
          <div className="space-y-8">
            <MatchResults 
              matchData={matchData}
              onGenerateRoadmap={handleGenerateRoadmap}
            />
            <SkillHeatmap data={matchData.heatmap_data} />
          </div>
        )}
        
        {step === 'roadmap' && roadmapData && (
          <LearningRoadmap 
            roadmapData={roadmapData}
            recommendations={recommendations}
            alternatives={alternatives}
          />
        )}
      </div>

      {/* Footer */}
      <footer className="border-t border-indigo-800/30 mt-20">
        <div className="container mx-auto px-4 py-8 text-center text-gray-400 text-sm">
          <p>Career Path Optimizer - AI-Powered Career Intelligence</p>
          <p className="mt-2">Transforming career guidance with semantic understanding</p>
        </div>
      </footer>
    </main>
  );
}
