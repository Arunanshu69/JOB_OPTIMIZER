'use client';

import { motion } from 'framer-motion';
import type { HeatmapSkill } from '@/types';

interface SkillHeatmapProps {
  data: HeatmapSkill[];
}

export default function SkillHeatmap({ data }: SkillHeatmapProps) {
  const getColorClasses = (color: string) => {
    switch (color) {
      case 'green':
        return 'bg-green-500/20 border-green-500/50 text-green-400';
      case 'red':
        return 'bg-red-500/20 border-red-500/50 text-red-400';
      case 'blue':
        return 'bg-blue-500/20 border-blue-500/50 text-blue-400';
      case 'yellow':
        return 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400';
      default:
        return 'bg-gray-500/20 border-gray-500/50 text-gray-400';
    }
  };

  const getStrengthLabel = (strength: string) => {
    switch (strength) {
      case 'high':
        return 'Strong';
      case 'medium':
        return 'Present';
      case 'low':
        return 'Weak';
      case 'missing':
        return 'Missing';
      default:
        return strength;
    }
  };

  // Group by domain
  const groupedSkills = data.reduce((acc, skill) => {
    const domain = skill.domain || 'General';
    if (!acc[domain]) {
      acc[domain] = [];
    }
    acc[domain].push(skill);
    return acc;
  }, {} as Record<string, HeatmapSkill[]>);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="max-w-6xl mx-auto"
    >
      <div className="bg-slate-800/50 border border-indigo-800/30 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-white mb-6">Skill Heatmap</h2>
        
        {/* Legend */}
        <div className="flex flex-wrap gap-4 mb-8 p-4 bg-slate-900/50 rounded-lg">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-green-500/50 border border-green-500"></div>
            <span className="text-sm text-gray-300">Strong Match</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-blue-500/50 border border-blue-500"></div>
            <span className="text-sm text-gray-300">Bonus Skill</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-red-500/50 border border-red-500"></div>
            <span className="text-sm text-gray-300">Missing</span>
          </div>
        </div>

        {/* Heatmap Grid by Domain */}
        <div className="space-y-8">
          {Object.entries(groupedSkills).map(([domain, skills], domainIdx) => (
            <motion.div
              key={domain}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * domainIdx }}
            >
              <h3 className="text-lg font-semibold text-indigo-400 mb-4">{domain}</h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                {skills.map((skill, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.05 * idx }}
                    whileHover={{ scale: 1.05 }}
                    className={`${getColorClasses(skill.color)} border rounded-lg p-3 cursor-pointer transition-all hover:shadow-lg`}
                    title={`${skill.skill} - ${getStrengthLabel(skill.strength)}\nIn Resume: ${skill.in_resume ? 'Yes' : 'No'}\nRequired: ${skill.in_job_requirement ? 'Yes' : 'No'}`}
                  >
                    <div className="text-sm font-medium truncate">{skill.skill}</div>
                    <div className="text-xs opacity-75 mt-1">{getStrengthLabel(skill.strength)}</div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Summary Stats */}
        <div className="mt-8 pt-6 border-t border-indigo-800/30">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">
                {data.filter(s => s.strength === 'high').length}
              </div>
              <div className="text-sm text-gray-400">Strong Skills</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">
                {data.filter(s => s.strength === 'medium').length}
              </div>
              <div className="text-sm text-gray-400">Present Skills</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-400">
                {data.filter(s => s.strength === 'missing').length}
              </div>
              <div className="text-sm text-gray-400">Missing Skills</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-indigo-400">
                {data.length}
              </div>
              <div className="text-sm text-gray-400">Total Skills</div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
