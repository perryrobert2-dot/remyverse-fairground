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
        <header className="text-center mb-16 px-4">
          <h1 className="text-5xl md:text-7xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-orange-400 mb-6 tracking-tighter">
            The Mystic's Matrix
          </h1>
          <p className="text-purple-300 font-serif italic text-xl max-w-2xl mx-auto">
            "Select your sign. Determine your fate. Try not to cry."
          </p>
        </header>
      )}

      <div className="max-w-7xl mx-auto px-6">
        
        {/* --- STATE 1: THE GALLERY (BIG CARDS) --- */}
        {!activeSign && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {issueData.mystic && Array.isArray(issueData.mystic) ? (
              issueData.mystic.map((item, index) => (
                <button 
                  key={index} 
                  onClick={() => setActiveSign(item)}
                  className="bg-slate-800 border-2 border-slate-700 rounded-3xl p-8 flex flex-col items-center justify-center hover:bg-slate-700 hover:border-orange-500 hover:scale-105 transition-all duration-300 group shadow-lg"
                >
                  {/* IMAGE CONTAINER - Now much larger (w-48 = 192px) */}
                  <div className="w-48 h-48 mb-6 relative p-4 bg-slate-900/50 rounded-full shadow-inner">
                      <img 
                        src={`${BUCKET_URL}${item.sign.toLowerCase()}.png`} 
                        alt={item.sign} 
                        className="w-full h-full object-contain drop-shadow-2xl group-hover:rotate-6 transition-transform duration-500"
                      />
                  </div>
                  
                  <span className="text-2xl font-black uppercase tracking-widest text-white group-hover:text-orange-400 transition-colors">
                    {item.sign}
                  </span>
                  
                  <span className="text-xs text-slate-500 mt-2 font-mono uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity">
                    Click to Reveal
                  </span>
                </button>
              ))
            ) : (
              <div className="col-span-full text-center text-2xl text-slate-500 font-serif italic">
                The Mystic is currently napping. Run the generator.
              </div>
            )}
          </div>
        )}

        {/* --- STATE 2: THE REVEAL (HUGE ART) --- */}
        {activeSign && (
          <div className="flex flex-col items-center justify-center min-h-[60vh] animate-fade-in-up">
            <div className="bg-slate-800 border-2 border-orange-500/50 p-10 rounded-[3rem] shadow-[0_0_100px_rgba(168,85,247,0.3)] max-w-2xl w-full text-center relative overflow-hidden">
                
                {/* Background Glow */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-gradient-to-b from-purple-900/20 to-transparent pointer-events-none"></div>

                {/* HUGE IMAGE (w-80 = 320px) */}
                <div className="w-80 h-80 mx-auto mb-8 relative">
                    <img 
                      src={`${BUCKET_URL}${activeSign.sign.toLowerCase()}.png`} 
                      alt={activeSign.sign} 
                      className="w-full h-full object-contain drop-shadow-[0_10px_20px_rgba(0,0,0,0.5)]"
                    />
                </div>
                
                <h2 className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-orange-300 to-purple-300 mb-8 uppercase tracking-widest">
                  {activeSign.sign}
                </h2>
                
                <div className="bg-slate-900/80 p-8 rounded-2xl border border-slate-700">
                  <p className="font-serif text-2xl text-orange-100 leading-relaxed italic">
                    "{activeSign.prediction}"
                  </p>
                </div>

                <button 
                  onClick={() => setActiveSign(null)}
                  className="mt-10 text-slate-400 hover:text-white uppercase tracking-[0.2em] text-sm font-bold border-b border-transparent hover:border-white transition-all"
                >
                  ← Choose Another Sign
                </button>
            </div>
          </div>
        )}

      </div>
    </main>
  );
}