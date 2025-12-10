import React, { useEffect, useState } from 'react';
import { getMyBadges, getMyCertificates, downloadCertificate } from '../../services/certifications';
import { Award, Download, Medal } from 'lucide-react';

const Achievements = () => {
  const [badges, setBadges] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [badgesData, certsData] = await Promise.all([getMyBadges(), getMyCertificates()]);
        setBadges(badgesData);
        setCertificates(certsData);
      } catch (error) {
        console.error("Error loading achievements", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="p-8">Loading Rewards...</div>;

  return (
    <div className="space-y-10">
      
      {/* --- BADGES SECTION --- */}
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Medal className="text-yellow-500" /> My Badges
        </h2>
        
        {badges.length === 0 ? (
            <div className="p-6 bg-gray-50 rounded-xl border border-gray-100 text-gray-500 text-sm">
                No badges yet. Complete lessons to earn them!
            </div>
        ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {badges.map((item) => (
                    <div key={item.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center text-center hover:shadow-md transition">
                        <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-3 text-2xl">
                            {/* Placeholder Emoji if no icon uploaded */}
                            {item.badge.icon ? <img src={item.badge.icon} className="w-10 h-10" /> : "🏆"}
                        </div>
                        <h3 className="font-bold text-gray-800">{item.badge.name}</h3>
                        <p className="text-xs text-gray-500 mt-1">{item.badge.description}</p>
                        <span className="mt-3 text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                            +{item.badge.xp_value} XP
                        </span>
                    </div>
                ))}
            </div>
        )}
      </div>

      {/* --- CERTIFICATES SECTION --- */}
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Award className="text-purple-600" /> My Certificates
        </h2>

        {certificates.length === 0 ? (
            <div className="p-6 bg-gray-50 rounded-xl border border-gray-100 text-gray-500 text-sm">
                Complete a course to earn your first certificate.
            </div>
        ) : (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                {certificates.map((cert) => (
                    <div key={cert.id} className="p-5 border-b border-gray-100 flex items-center justify-between last:border-0 hover:bg-gray-50">
                        <div className="flex items-center gap-4">
                            <div className="bg-green-100 p-3 rounded-lg text-green-700">
                                <Award size={24} />
                            </div>
                            <div>
                                <h3 className="font-bold text-gray-800">{cert.course_name}</h3>
                                <p className="text-xs text-gray-500">Issued on {new Date(cert.issued_at).toLocaleDateString()}</p>
                            </div>
                        </div>
                        
                        <button 
                            onClick={() => downloadCertificate(cert.id, `Certificate-${cert.course_name}.pdf`)}
                            className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white text-sm rounded-lg hover:bg-slate-800 transition"
                        >
                            <Download size={16} /> Download PDF
                        </button>
                    </div>
                ))}
            </div>
        )}
      </div>

    </div>
  );
};

export default Achievements;