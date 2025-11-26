import React from 'react';
import Link from 'next/link';
import issueData from "./data/current_issue.json";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#FDFBF7] text-slate-800 font-sans selection:bg-orange-200 pb-20">
      
      {/* --- HEADER --- */}
      <nav className="border-b-2 border-slate-900 bg-white py-6">
        <div className="max-w-4xl mx-auto px-6 text-center">
            <h1 className="text-3xl font-black uppercase tracking-tighter">The Remy Digest</h1>
            <p className="text-xs font-bold tracking-widest text-slate-500 mt-1">THE NORTHERN BEACHES' ONLY RELIABLE SOURCE</p>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-4 py-12">
        
        {/* HERO IMAGE */}
        <section className="border-2 border-slate-900 rounded-lg overflow-hidden bg-white mb-12 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
           <img src={issueData.imagePath} alt={issueData.headline} className="w-full h-auto object-cover"/>
        </section>

        {/* HEADLINE & ARTICLE */}
        <div className="max-w-3xl mx-auto">
            <article className="text-center mb-12">
            <span className="inline-block bg-slate-900 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-4">{issueData.category}</span>
            <h2 className="text-4xl md:text-5xl font-black text-slate-900 mb-6 leading-tight">{issueData.headline}</h2>
            <p className="text-xl md:text-2xl text-slate-600 font-serif italic leading-relaxed">"{issueData.subtext}"</p>
            </article>

            <article className="mb-16 font-serif text-lg leading-relaxed text-slate-800 border-b-2 border-slate-200 pb-12">
            {issueData.body && issueData.body.split('\n').map((paragraph, index) => (
                paragraph.trim() !== "" && (<p key={index} className="mb-6">{paragraph}</p>)
            ))}
            <div className="flex justify-center mt-8"><span className="text-slate-400 tracking-widest text-xs uppercase">*** End of Report ***</span></div>
            </article>
        </div>

        {/* --- FEATURE ROW: PROFESSOR & MYSTIC --- */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20">
            
            {/* LEFT COL: The Professor (Beige Card) */}
            <div className="bg-[#F2EFE9] border-2 border-slate-900 rounded-xl p-6 flex flex-col shadow-sm h-full">
                <div className="flex items-center gap-4 mb-4 border-b-2 border-slate-300 pb-4">
                    <div className="w-16 h-16 rounded-full border-2 border-slate-900 overflow-hidden bg-white shrink-0">
                        <img src="/images/professor.png" alt="Professor Remy" className="w-full h-full object-cover"/>
                    </div>
                    <div>
                        <h3 className="font-bold text-slate-900 uppercase tracking-wider text-sm">From The Archives</h3>
                        <p className="text-xs text-slate-500 font-mono">PROF. REMY</p>
                    </div>
                </div>
                <div className="flex-1">
                    <p className="text-md text-slate-800 leading-relaxed font-serif italic">"{issueData.professor.content}"</p>
                </div>
            </div>

            {/* RIGHT COL: The Mystic (Purple Card) */}
            <Link href="/mystic" className="group h-full">
                <div className="bg-slate-900 border-2 border-slate-900 rounded-xl p-6 flex flex-col items-center justify-center text-center shadow-sm h-full transition-transform group-hover:-translate-y-1 relative overflow-hidden">
                    {/* Background decoration */}
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 to-orange-500"></div>
                    
                    <div className="w-24 h-24 rounded-full border-2 border-orange-400/50 overflow-hidden mb-4 shadow-[0_0_15px_rgba(168,85,247,0.4)] group-hover:shadow-[0_0_25px_rgba(168,85,247,0.6)] transition-shadow">
                        <img src="/images/mystic_link.png" alt="Mystic" className="w-full h-full object-cover opacity-90 group-hover:opacity-100"/>
                    </div>
                    
                    <h3 className="text-xl font-black text-white uppercase tracking-widest mb-1 group-hover:text-orange-400 transition-colors">Consult The Stars</h3>
                    <p className="text-xs text-purple-300 font-mono">YOUR DOOM AWAITS →</p>
                </div>
            </Link>

        </div>

        {/* --- THE BARKER CLASSIFIEDS --- */}
        <section className="border-t-4 border-double border-slate-300 pt-12">
            <div className="flex items-center justify-center gap-6 mb-10">
                <div className="w-20 h-20 rounded-full border-2 border-slate-900 overflow-hidden bg-white shrink-0">
                    <img src="/images/newsboy.png" alt="Newsboy" className="w-full h-full object-cover"/>
                </div>
                <h3 className="text-3xl font-black uppercase text-slate-900 tracking-tighter">The Barker Classifieds</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {issueData.classifieds && issueData.classifieds.map((ad, index) => (
                    <div key={index} className="bg-white border border-slate-200 p-4 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-8 h-8 bg-slate-100 -mr-4 -mt-4 transform rotate-45"></div>
                        <p className="font-mono text-xs text-slate-400 mb-2 uppercase tracking-widest">Ref: #{1000 + index}</p>
                        <p className="font-serif text-sm leading-relaxed text-slate-800 font-bold">{ad}</p>
                    </div>
                ))}
            </div>
        </section>

      </div>
    </main>
  );
}