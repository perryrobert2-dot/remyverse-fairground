'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function AdvicePage() {
  const [data, setData] = useState<any>(null);
  const [openLetter, setOpenLetter] = useState<string | null>(null);

  useEffect(() => { fetch('/data/current_issue.json').then(r => r.json()).then(setData); }, []);
  if (!data) return <div className="p-20 text-center bg-[#e8f4bc] text-black">Loading...</div>;

  const advice = data.advice || {};

  return (
    <main className="min-h-screen bg-[#e8f4bc] p-4 font-sans selection:bg-pink-300">
      <nav className="mb-8"><Link href="/" className="font-bold uppercase text-xs border-2 border-black px-4 py-2 bg-white text-black hover:bg-pink-200 transition-colors">← Back to Safety</Link></nav>
      
      <header className="text-center mb-12">
        <h1 className="text-4xl md:text-6xl font-black uppercase text-pink-600 drop-shadow-[4px_4px_0px_rgba(0,0,0,1)] stroke-black mb-2">The Tea Room</h1>
        <p className="font-serif italic text-black">"If you have a problem, I have a snap."</p>
      </header>

      <div className="max-w-3xl mx-auto grid gap-6">
        {/* MAIN LETTER */}
        <div onClick={() => setOpenLetter('main')} className="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-6 cursor-pointer hover:bg-pink-50 hover:-translate-y-1 transition-all">
             <span className="bg-red-500 text-white text-xs font-black uppercase px-2 py-1 mb-2 inline-block rotate-2">Hot Topic</span>
             <h2 className="font-bold text-xl mb-2 text-black">"{advice.main_q || 'Waiting for question...'}"</h2>
             <p className="font-mono text-xs text-black uppercase tracking-widest">— {advice.main_pseudo || 'Anonymous'}</p>
        </div>

        {/* SNAPS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div onClick={() => setOpenLetter('snap1')} className="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-6 cursor-pointer hover:bg-blue-50 hover:-translate-y-1 transition-all">
                <h2 className="font-bold text-lg mb-2 text-black">"{advice.snap1_q || '...'}"</h2>
                <p className="font-mono text-xs text-black uppercase tracking-widest">— {advice.snap1_pseudo || 'Anonymous'}</p>
            </div>
            <div onClick={() => setOpenLetter('snap2')} className="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-6 cursor-pointer hover:bg-yellow-50 hover:-translate-y-1 transition-all">
                <h2 className="font-bold text-lg mb-2 text-black">"{advice.snap2_q || '...'}"</h2>
                <p className="font-mono text-xs text-black uppercase tracking-widest">— {advice.snap2_pseudo || 'Anonymous'}</p>
            </div>
        </div>
      </div>

      {/* MODAL */}
      {openLetter && (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4" onClick={() => setOpenLetter(null)}>
            <div className="bg-[#fffdf0] max-w-lg w-full p-8 border-4 border-black shadow-[20px_20px_0px_0px_rgba(255,255,255,0.2)] relative" onClick={e => e.stopPropagation()}>
                <button onClick={() => setOpenLetter(null)} className="absolute top-4 right-4 font-black text-xl hover:text-red-600 text-black">X</button>
                <div className="mb-6 border-b-2 border-black/10 pb-4">
                    <span className="font-mono text-xs text-black uppercase tracking-widest mb-1 block">The Query:</span>
                    <h3 className="font-bold text-xl italic text-black">
                        "{openLetter === 'main' ? advice.main_q : openLetter === 'snap1' ? advice.snap1_q : advice.snap2_q}"
                    </h3>
                </div>
                <div>
                    <span className="font-mono text-xs text-pink-600 uppercase tracking-widest mb-2 block font-black">Auntie Says:</span>
                    <p className="font-serif text-xl leading-relaxed whitespace-pre-line text-black">
                        {openLetter === 'main' ? advice.main_a : openLetter === 'snap1' ? advice.snap1_a : advice.snap2_a}
                    </p>
                </div>
            </div>
        </div>
      )}
    </main>
  );
}