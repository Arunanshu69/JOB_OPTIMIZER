'use client';

import { motion } from 'framer-motion';
import { Target, TrendingUp, Loader2, CheckCircle, XCircle, Plus } from 'lucide-react';
import { generateRoadmap, getAlternativeCareers, getCareerCounseling } from '@/lib/api';
import { useState } from 'react';
import type {
  MatchData,
  RoadmapData,
  CourseRecommendation,
  AlternativeCareer,
  CertificationRecommendation,
} from '@/types';

interface MatchResultsProps {
  matchData: MatchData;
  onGenerateRoadmap: (
    roadmap: RoadmapData,
    recommendations: CourseRecommendation[],
    alternatives: AlternativeCareer[],
    certifications: CertificationRecommendation[]
  ) => void;
}

export default function MatchResults({ matchData, onGenerateRoadmap }: MatchResultsProps) {
  const [generating, setGenerating] = useState(false);

  const handleGenerateRoadmap = async () => {
    setGenerating(true);
    try {
      const targetRole = matchData.job_title || 'Your Target Role';
      const rawSkills =
        matchData.skill_breakdown_raw?.resume_skills ??
        matchData.skill_breakdown.resume_skills.map((skill) =>
          skill.toLowerCase().replace(/\s+/g, '_')
        );
      const result = await generateRoadmap(
        matchData.skill_breakdown.missing_skills,
        targetRole,
        rawSkills
      );
      const alternativesResult = await getAlternativeCareers(rawSkills, targetRole);
      const counselorResult = await getCareerCounseling(rawSkills, targetRole);
      onGenerateRoadmap(
        result.roadmap,
        result.recommendations,
        alternativesResult.alternatives || [],
        counselorResult.certifications || []
      );
    } catch (error) {
      console.error('Error generating roadmap:', error);
    } finally {
      setGenerating(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreBackground = (score: number) => {
    if (score >= 80) return 'from-green-500/20 to-green-600/20 border-green-500/50';
    if (score >= 60) return 'from-yellow-500/20 to-yellow-600/20 border-yellow-500/50';
    return 'from-red-500/20 to-red-600/20 border-red-500/50';
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Match Score Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className={`bg-gradient-to-br ${getScoreBackground(matchData.match_score)} border rounded-xl p-8 text-center backdrop-blur-sm`}
      >
        <h2 className="text-2xl font-semibold text-white mb-4">Overall Match Score</h2>
        <div className="relative inline-flex items-center justify-center">
          <div className="w-48 h-48 rounded-full border-8 border-white/20 flex items-center justify-center">
            <div>
              <div className={`text-6xl font-bold ${getScoreColor(matchData.match_score)}`}>
                {matchData.match_score}%
              </div>
              <div className="text-gray-300 text-sm mt-2">Compatibility</div>
            </div>
          </div>
        </div>
        
        <div className="mt-6 grid grid-cols-2 gap-4 max-w-md mx-auto">
          <div className="bg-slate-900/50 rounded-lg p-4">
            <div className="text-2xl font-bold text-indigo-400">{matchData.semantic_similarity}%</div>
            <div className="text-sm text-gray-300">Semantic Match</div>
          </div>
          <div className="bg-slate-900/50 rounded-lg p-4">
            <div className="text-2xl font-bold text-cyan-400">{matchData.skill_match_percentage}%</div>
            <div className="text-sm text-gray-300">Skill Match</div>
          </div>
        </div>
      </motion.div>

      {/* Explanation */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-slate-800/50 border border-indigo-800/30 rounded-xl p-6"
      >
        <h3 className="text-xl font-semibold text-white mb-3 flex items-center gap-2">
          <Target className="w-5 h-5 text-indigo-400" />
          Analysis Summary
        </h3>
        <p className="text-gray-300 leading-relaxed">{matchData.explanation}</p>
      </motion.div>

      {/* Skill Breakdown */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        {/* Matched Skills */}
        <div className="bg-slate-800/50 border border-green-800/30 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5 text-green-400" />
            <h3 className="text-lg font-semibold text-white">Matched Skills</h3>
          </div>
          <div className="text-3xl font-bold text-green-400 mb-2">
            {matchData.skill_breakdown.matched_skills.length}
          </div>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {matchData.skill_breakdown.matched_skills.map((skill, idx) => (
              <div key={idx} className="bg-green-500/10 rounded px-3 py-1 text-sm text-green-300">
                {skill}
              </div>
            ))}
          </div>
        </div>

        {/* Missing Skills */}
        <div className="bg-slate-800/50 border border-red-800/30 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <XCircle className="w-5 h-5 text-red-400" />
            <h3 className="text-lg font-semibold text-white">Missing Skills</h3>
          </div>
          <div className="text-3xl font-bold text-red-400 mb-2">
            {matchData.skill_breakdown.missing_skills.length}
          </div>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {matchData.skill_breakdown.missing_skills.map((skill, idx) => (
              <div key={idx} className="bg-red-500/10 rounded px-3 py-1 text-sm text-red-300">
                {skill}
              </div>
            ))}
          </div>
        </div>

        {/* Additional Skills */}
        <div className="bg-slate-800/50 border border-blue-800/30 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Plus className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-semibold text-white">Bonus Skills</h3>
          </div>
          <div className="text-3xl font-bold text-blue-400 mb-2">
            {matchData.skill_breakdown.additional_skills.length}
          </div>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {matchData.skill_breakdown.additional_skills.map((skill, idx) => (
              <div key={idx} className="bg-blue-500/10 rounded px-3 py-1 text-sm text-blue-300">
                {skill}
              </div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Generate Roadmap Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="text-center"
      >
        <button
          onClick={handleGenerateRoadmap}
          disabled={generating}
          className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:cursor-not-allowed text-white font-medium px-8 py-4 rounded-lg transition-colors flex items-center justify-center gap-2 mx-auto"
        >
          {generating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating Roadmap...
            </>
          ) : (
            <>
              <TrendingUp className="w-5 h-5" />
              Generate Growth Roadmap
            </>
          )}
        </button>
      </motion.div>
    </div>
  );
}
