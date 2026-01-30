import React, { useEffect, useState } from 'react';

const Skills = () => {
    const [skills, setSkills] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/api/skills')
            .then(res => res.json())
            .then(data => {
                setSkills(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch skills:", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="p-8 text-white">Loading Skills...</div>;

    return (
        <div className="p-8 bg-gray-900 min-h-screen text-white">
            <h1 className="text-3xl font-bold mb-6">Skills Manager 🛠️</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {skills.map((skill) => (
                    <div key={skill.name} className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-xl">
                        <div className="flex justify-between items-start mb-4">
                            <h2 className="text-xl font-semibold text-blue-400">{skill.name}</h2>
                            <RiskBadge level={skill.risk_level} />
                        </div>
                        <p className="text-gray-300 text-sm mb-4 h-16">{skill.description}</p>

                        <div className="bg-gray-900 rounded p-2 text-xs font-mono text-gray-500">
                            {Object.keys(skill.parameters).join(", ")}
                        </div>

                        <div className="mt-4 flex justify-end">
                            <button className={`px-3 py-1 rounded text-sm font-medium ${skill.enabled ? 'bg-green-600' : 'bg-red-600'}`}>
                                {skill.enabled ? 'Enabled' : 'Disabled'}
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

const RiskBadge = ({ level }) => {
    let color = "bg-gray-600";
    if (level === "SAFE") color = "bg-green-500";
    if (level === "MEDIUM") color = "bg-yellow-600";
    if (level === "HIGH") color = "bg-red-600";

    return (
        <span className={`${color} text-xs font-bold px-2 py-1 rounded`}>
            {level}
        </span>
    );
};

export default Skills;
