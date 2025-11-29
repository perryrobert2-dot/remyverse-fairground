'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function HoroscopesPage() {
  const [data, setData] = useState<any>(null);
  const [selectedSign, setSelectedSign] = useState<any>(null);

  useEffect(() => { fetch('/data/current_issue.json').then(r => r.json()).then(setData); }, []);
  if (!data) return <div className="p-20 text-center bg-slate-900 text-purple-300">Consulting the Stars...</div>;

  return (
    <main className="min-h-screen bg-slate-900 text-purple-100 font-sans p-4 relative overflow-hidden">
      <div className="fixed inset-0 opacity-10 pointer-events-none bg-[url('https://www.transparenttextures.com/patterns/stardust.png')]"></div>
      
      <nav className="relative z-10 mb-8 flex justify-between items-center">
         <Link href="/" className="font-bold text-xs uppercase tracking-widest border border-purple-500/50 px-4 py-2 hover:bg-purple-500/20 transition-colors">← Earth</Link>
         <span className="font-mono text-xs text-purple-500">The Void</span>
      </nav>

      <div className="max-w-5xl mx-auto relative z-10">
         <header className="text-center mb-12">
            <h1 className="text-4xl md:text-6xl font-black uppercase text-transparent bg-clip-text bg-gradient-to-b from-purple-300 to-purple-900 mb-2">The Star Chart</h1>
            <p className="font-serif italic text-purple-400/60">"Fate is just a suggestion."</p>
         </header>

         <div className="grid grid-cols-3 md:grid-cols-4 gap-4">
            {data.horoscopes?.map((h: any) => (
                <button key={h.sign} onClick={() => setSelectedSign(h)} className="group relative aspect-square bg-slate-800/50 border border-purple-500/30 rounded-full flex flex-col items-center justify-center hover:bg-purple-900/40 hover:border-purple-400 transition-all hover:scale-105">
                    <img src={h.icon} alt={h.sign} className="w-10 h-10 mb-2 opacity-70 group-hover:opacity-100 transition-opacity" />
                    <span className="font-mono text-[10px] uppercase tracking-widest text-purple-300 group-hover:text-white">{h.sign}</span>
                </button>
            ))}
         </div>
      </div>

      {/* READING MODAL */}
      {selectedSign && (
         <div className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-6 backdrop-blur-sm" onClick={() => setSelectedSign(null)}>
            <div className="max-w-xl w-full text-center relative" onClick={e => e.stopPropagation()}>
                <button onClick={() => setSelectedSign(null)} className="absolute -top-12 right-0 text-purple-500 hover:text-white text-xl">CLOSE [X]</button>
                <img src={selectedSign.icon} className="w-24 h-24 mx-auto mb-6 drop-shadow-[0_0_15px_rgba(168,85,247,0.5)] animate-pulse" />
                
                {/* SIZED DOWN TO 4XL */}
                <h2 className="text-4xl md:text-6xl font-black uppercase text-white mb-6 tracking-tighter">{selectedSign.sign}</h2>
                
                <div className="bg-slate-800/80 border border-purple-500/30 p-8 rounded-2xl max-h-[60vh] overflow-y-auto">
                    <p className="font-serif text-xl md:text-2xl leading-relaxed text-purple-100">
                        "{selectedSign.prediction}"
                    </p>
                </div>
            </div>
         </div>
      )}
    </main>
  );
}