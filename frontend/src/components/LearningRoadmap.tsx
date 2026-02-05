'use client';

import { motion } from 'framer-motion';
import { Calendar, Clock, Award, ExternalLink } from 'lucide-react';
import type { RoadmapData, CourseRecommendation, AlternativeCareer } from '@/types';

interface LearningRoadmapProps {
  roadmapData: RoadmapData;
  recommendations: CourseRecommendation[];
  alternatives: AlternativeCareer[];
}

export default function LearningRoadmap({
  roadmapData,
  recommendations,
  alternatives,
}: LearningRoadmapProps) {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h2 className="text-4xl font-bold text-white mb-4">
          Your <span className="text-indigo-400">6-Month</span> Learning Roadmap
        </h2>
        <p className="text-xl text-gray-300">
          Personalized plan to bridge your skill gaps for {roadmapData.target_role}
        </p>
      </motion.div>

      {/* Timeline */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-slate-800/50 border border-indigo-800/30 rounded-xl p-8"
      >
        <h3 className="text-2xl font-semibold text-white mb-6 flex items-center gap-2">
          <Calendar className="w-6 h-6 text-indigo-400" />
          Monthly Milestones
        </h3>

        <div className="space-y-6">
          {roadmapData.milestones.map((milestone, idx) => (
            <motion.div
              key={milestone.month}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * idx }}
              className="relative pl-8 pb-6 border-l-2 border-indigo-600/50 last:border-l-0"
            >
              {/* Timeline Dot */}
              <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-indigo-600 border-4 border-slate-900"></div>

              {/* Content */}
              <div className="bg-slate-900/50 rounded-lg p-6 border border-indigo-800/20">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="text-sm text-indigo-400 font-medium mb-1">
                      Month {milestone.month}
                    </div>
                    <h4 className="text-lg font-semibold text-white">
                      {milestone.title}
                    </h4>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-400">
                    <Clock className="w-4 h-4" />
                    {milestone.estimated_hours}h
                  </div>
                </div>

                {/* Skills */}
                <div className="flex flex-wrap gap-2">
                  {milestone.skills.map((skill, skillIdx) => (
                    <span
                      key={skillIdx}
                      className="bg-indigo-500/20 text-indigo-300 px-3 py-1 rounded-full text-sm border border-indigo-500/30"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Course Recommendations */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-slate-800/50 border border-indigo-800/30 rounded-xl p-8"
      >
        <h3 className="text-2xl font-semibold text-white mb-6 flex items-center gap-2">
          <Award className="w-6 h-6 text-indigo-400" />
          Recommended Courses
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {recommendations.map((rec, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.05 * idx }}
              className="bg-slate-900/50 rounded-lg p-6 border border-indigo-800/20 hover:border-indigo-600/50 transition-colors"
            >
              {/* Skill Tag */}
              <div className="inline-block bg-indigo-500/20 text-indigo-300 px-3 py-1 rounded-full text-sm font-medium mb-3">
                {rec.skill}
              </div>

              {/* Course Name */}
              <h4 className="text-lg font-semibold text-white mb-2">
                {rec.course_name}
              </h4>

              {/* Platform and Duration */}
              <div className="flex items-center gap-4 text-sm text-gray-400 mb-4">
                <span>{rec.platform}</span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {rec.duration}
                </span>
              </div>

              {/* ROI and Relevance */}
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="text-xs text-gray-400 mb-1">ROI Score</div>
                  <div className="text-2xl font-bold text-green-400">{rec.roi_score}</div>
                </div>
                <div>
                  <div className="text-xs text-gray-400 mb-1">Relevance</div>
                  <div className="text-sm font-medium text-indigo-400">{rec.relevance}</div>
                </div>
              </div>

              {/* CTA Button */}
              <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 rounded-lg transition-colors flex items-center justify-center gap-2">
                <ExternalLink className="w-4 h-4" />
                Explore Course
              </button>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Alternative Careers */}
      {alternatives.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="bg-slate-800/50 border border-indigo-800/30 rounded-xl p-8"
        >
          <h3 className="text-2xl font-semibold text-white mb-6 flex items-center gap-2">
            <Award className="w-6 h-6 text-indigo-400" />
            Alternative Career Paths
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {alternatives.map((alt, idx) => (
              <motion.div
                key={`${alt.role}-${idx}`}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.05 * idx }}
                className="bg-slate-900/50 rounded-lg p-6 border border-indigo-800/20"
              >
                <div className="flex items-start justify-between mb-3">
                  <h4 className="text-lg font-semibold text-white">{alt.role}</h4>
                  <span className="text-sm text-indigo-300">
                    {alt.match_percentage}% fit
                  </span>
                </div>
                <p className="text-sm text-gray-400 mb-4">{alt.reason}</p>
                <div className="text-xs text-gray-400 mb-2">Matched Skills</div>
                <div className="flex flex-wrap gap-2 mb-3">
                  {alt.matched_skills.map((skill, skillIdx) => (
                    <span
                      key={skillIdx}
                      className="bg-green-500/10 text-green-300 px-2 py-1 rounded-full text-xs border border-green-500/30"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
                <div className="text-xs text-gray-400 mb-2">Skills To Add</div>
                <div className="flex flex-wrap gap-2">
                  {alt.missing_skills.slice(0, 6).map((skill, skillIdx) => (
                    <span
                      key={skillIdx}
                      className="bg-red-500/10 text-red-300 px-2 py-1 rounded-full text-xs border border-red-500/30"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Action Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-gradient-to-br from-indigo-600/20 to-purple-600/20 border border-indigo-500/50 rounded-xl p-8 text-center"
      >
        <h3 className="text-2xl font-bold text-white mb-2">Ready to Start?</h3>
        <p className="text-gray-300 mb-6">
          Follow this roadmap to bridge your skill gaps and land your dream role
        </p>
        <div className="flex flex-wrap items-center justify-center gap-4">
          <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-8 py-3 rounded-lg transition-colors">
            Download Roadmap
          </button>
          <button className="bg-slate-700 hover:bg-slate-600 text-white font-medium px-8 py-3 rounded-lg transition-colors">
            Track Progress
          </button>
        </div>
      </motion.div>
    </div>
  );
}
