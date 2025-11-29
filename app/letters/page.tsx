'use client';
import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';

export default function LettersPage() {
  const [data, setData] = useState<any>(null);
  const [selectedLetter, setSelectedLetter] = useState<any>(null);

  useEffect(() => { fetch('/data/current_issue.json').then(r => r.json()).then(setData); }, []);
  if (!data) return <div className="p-20 text-center font-serif text-black">Opening the mailbag...</div>;

  const letters = data.letters || [];

  return (
    <main className="min-h-screen bg-[#f0e6d2] text-[#1a1a1a] p-4 md:p-12 font-serif">
      
      <nav className="mb-8 border-b-2 border-black/20 pb-4 flex justify-between items-end">
        <Link href="/" className="font-sans text-xs font-bold uppercase tracking-widest hover:text-red-700 transition-colors text-black">← Front Page</Link>
        <div className="text-right">
             <h1 className="font-black text-2xl md:text-5xl uppercase tracking-tighter leading-none text-black">The Mailbag</h1>
             <span className="font-sans text-xs font-bold uppercase tracking-widest text-black">Voice of the People</span>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto">
        
        {/* HERO IMAGE - CONSTRAINED WIDTH */}
        {/* Changed w-full to max-w-3xl to stop the stretching */}
        <div className="mb-12 relative h-64 md:h-80 max-w-3xl mx-auto border-4 border-black shadow-[10px_10px_0px_0px_rgba(0,0,0,0.2)] bg-white">
            <Image src="/personas/mail_carrier.jpg" alt="Mail Carrier" fill className="object-cover object-top" />
            <div className="absolute bottom-2 left-2 bg-white/90 px-3 py-1 border-2 border-black">
                <span className="font-bold font-sans text-[10px] uppercase tracking-widest text-red-600 block">On Duty:</span>
                <span className="font-bold text-sm block text-black leading-none">Remy The Postie</span>
            </div>
        </div>

        {/* CLICKABLE CARDS */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {letters.map((letter: any, i: number) => (
                <div key={i} onClick={() => setSelectedLetter(letter)} className="bg-white p-6 shadow-md border-t-8 border-red-700 relative cursor-pointer hover:-translate-y-2 transition-all overflow-hidden group">
                    
                    {/* STAMP */}
                    <div className="absolute top-3 right-3 w-16 h-16 rotate-3 z-10">
                        <div className="relative w-full h-full border-[3px] border-dotted border-slate-300 bg-[#fdfdf8] shadow-sm overflow-hidden p-0.5">
                             <Image src="/images/stamp.jpg" alt="Postage Stamp" fill className="object-cover" />
                        </div>
                        <div className="absolute inset-0 pointer-events-none opacity-70 mix-blend-multiply">
                             <div className="absolute top-1/3 -left-2 -right-2 h-[2px] bg-black rotate-[-15deg] shadow-[0_4px_0_black]"></div>
                             <div className="absolute top-1/3 -left-2 -right-2 h-[2px] bg-black rotate-[-15deg] shadow-[0_8px_0_black] mt-1"></div>
                        </div>
                    </div>

                    <span className="font-sans text-[10px] font-bold uppercase tracking-widest text-black/60 mb-2 block relative z-0">Letter #{i+1}</span>
                    <h2 className="font-bold text-xl leading-tight mb-2 text-black line-clamp-3 relative z-0 pr-12">{letter.topic}</h2>
                    <div className="mt-4 pt-4 border-t border-black/10 relative z-0">
                        <span className="font-sans text-xs font-bold uppercase tracking-widest text-red-700 block mb-1">From:</span>
                        <span className="font-bold text-sm text-black">{letter.author}</span>
                    </div>
                    <div className="absolute bottom-2 right-2 text-xs font-bold text-black/40 uppercase relative z-0 group-hover:text-red-600 transition-colors">Click to Read ↘</div>
                </div>
            ))}
        </div>

        {/* READING MODAL - NOW SCROLLABLE */}
        {selectedLetter && (
            <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4" onClick={() => setSelectedLetter(null)}>
                <div className="bg-[#fcfbf9] max-w-lg w-full max-h-[85vh] overflow-y-auto p-8 border-4 border-black shadow-2xl relative" onClick={e => e.stopPropagation()}>
                    <button onClick={() => setSelectedLetter(null)} className="absolute top-4 right-4 font-black text-xl hover:text-red-600 text-black z-50">X</button>
                    
                    <span className="font-sans text-xs font-bold uppercase tracking-widest text-red-700 mb-2 block">Topic:</span>
                    <h2 className="font-black text-2xl leading-tight mb-6 text-black border-b-2 border-black pb-4">{selectedLetter.topic}</h2>
                    
                    <p className="font-serif text-lg leading-relaxed text-black whitespace-pre-line mb-8">
                        "{selectedLetter.body}"
                    </p>
                    
                    <div className="text-right">
                        <span className="font-sans text-xs font-bold uppercase tracking-widest text-black/60">Signed,</span>
                        <div className="font-bold text-black">{selectedLetter.author}</div>
                    </div>
                </div>
            </div>
        )}

      </div>
    </main>
  );
}