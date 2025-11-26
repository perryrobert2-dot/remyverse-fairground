"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import issueData from "../data/current_issue.json";

// CONFIG: Your Bucket URL
const BUCKET_URL = "https://storage.googleapis.com/remys-digest-public-assets/";

export default function MysticTent() {
  const [activeSign, setActiveSign] = useState<any | null>(null);

  return (
    <main className="min-h-screen bg-slate-900 text-orange-100 font-sans pb-20">
      
      {/* NAVIGATION */}
      <nav className="p-6 flex justify-between items-center">
        <Link href="/" className="text-orange-300 hover:text-white uppercase tracking-widest text-xs font-bold">
          ← Back to Fairground
        </Link>
        {activeSign && (
          <button onClick={() => setActiveSign(null)} className="text-orange-300 hover:text-white uppercase tracking-widest text-xs font-bold">
            ✕ Close Reading
          </button>
        )}
      </nav>

      {/* HEADER */}
      {!activeSign && (
        <header className="text-center mb-12">
          <h1 className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-orange-400 mb-4">
            The Mystic's Matrix
          </h1>
          <p className="text-purple-300 font-serif italic text-xl">
            "Select your sign. Determine your fate."
          </p>
        </header>
      )}

      <div className="max-w-4xl mx-auto px-4">
        
        {/* --- STATE 1: THE MATRIX (GRID OF ICONS) --- */}
        {!activeSign && (
          <div className="grid grid-cols-3 md:grid-cols-4 gap-6">
            {issueData.mystic && Array.isArray(issueData.mystic) ? (
              issueData.mystic.map((item, index) => (
                <button 
                  key={index} 
                  onClick={() => setActiveSign(item)}
                  className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex flex-col items-center justify-center hover:bg-slate-700 hover:border-orange-500/50 transition-all group"
                >
                  <div className="w-16 h-16 mb-2">
                      <img src={`${BUCKET_URL}${item.sign.toLowerCase()}.png`} alt={item.sign} className="w-full h-full object-contain opacity-70 group-hover:opacity-100 transition-opacity"/>
                  </div>
                  <span className="text-xs font-bold uppercase tracking-widest text-slate-400 group-hover:text-orange-300">
                    {item.sign}
                  </span>
                </button>
              ))
            ) : (
              <div className="col-span-full text-center">The Mystic is sleeping.</div>
            )}
          </div>
        )}

        {/* --- STATE 2: THE REVEAL (SINGLE CARD) --- */}
        {activeSign && (
          <div className="flex flex-col items-center justify-center min-h-[50vh] animate-fade-in-up">
            <div className="bg-slate-800 border-2 border-orange-500/30 p-8 rounded-3xl shadow-[0_0_50px_rgba(168,85,247,0.2)] max-w-md text-center relative">
                
                {/* Glow effect */}
                <div className="absolute -top-10 left-1/2 -translate-x-1/2 w-32 h-32 bg-purple-500/20 rounded-full blur-3xl pointer-events-none"></div>

                <div className="w-32 h-32 mx-auto mb-6 relative">
                    <img src={`${BUCKET_URL}${activeSign.sign.toLowerCase()}.png`} alt={activeSign.sign} className="w-full h-full object-contain drop-shadow-lg"/>
                </div>
                
                <h2 className="text-4xl font-black text-white mb-6 uppercase tracking-wider">
                  {activeSign.sign}
                </h2>
                
                <p className="font-serif text-xl text-orange-100 leading-relaxed italic mb-8">
                  "{activeSign.prediction}"
                </p>

                <button 
                  onClick={() => setActiveSign(null)}
                  className="bg-slate-900 text-slate-400 hover:text-white px-6 py-2 rounded-full text-xs font-bold uppercase tracking-widest border border-slate-700 hover:border-white transition-all"
                >
                  Choose Another Sign
                </button>
            </div>
          </div>
        )}

      </div>
    </main>
  );
}