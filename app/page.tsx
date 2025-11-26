import React from 'react';
import Link from 'next/link';
import issueData from "./data/current_issue.json";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#FDFBF7] text-slate-800 font-sans pb-20">
      
      {/* --- HEADER --- */}
      <nav className="border-b-2 border-slate-900 bg-white py-6">
        <div className="max-w-4xl mx-auto px-6 text-center">
            <h1 className="text-3xl font-black uppercase tracking-tighter">The Remy Digest</h1>
            <p className="text-xs font-bold tracking-widest text-slate-500 mt-1">THE NORTHERN BEACHES' ONLY RELIABLE SOURCE</p>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 py-12">
        
        {/* HERO IMAGE */}
        <section className="border-2 border-slate-900 rounded-lg overflow-hidden bg-white mb-12">
           <img src={issueData.imagePath} alt={issueData.headline} className="w-full h-auto object-cover"/>
        </section>

        {/* HEADLINE */}
        <article className="max-w-2xl mx-auto text-center mb-12">
          <span className="inline-block bg-slate-900 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">{issueData.category}</span>
          <h2 className="text-4xl md:text-5xl font-black text-slate-900 mb-6 leading-tight">{issueData.headline}</h2>
          <p className="text-xl md:text-2xl text-slate-600 font-serif italic leading-relaxed">"{issueData.subtext}"</p>
        </article>

        {/* MAIN ARTICLE BODY */}
        <article className="max-w-2xl mx-auto mb-16 font-serif text-lg leading-relaxed text-slate-800">
           {issueData.body && issueData.body.split('\n').map((paragraph, index) => (
             paragraph.trim() !== "" && (<p key={index} className="mb-6">{paragraph}</p>)
           ))}
           <div className="flex justify-center mt-8"><span className="text-slate-400 tracking-widest text-xs uppercase">*** End of Report ***</span></div>
        </article>

        {/* --- PROFESSOR'S CORNER --- */}
        <section className="max-w-2xl mx-auto mt-16 mb-20">
           <div className="flex items-center gap-3 mb-4">
              <div className="h-[2px] bg-slate-300 flex-1"></div>
              <span className="text-xs font-bold uppercase tracking-widest text-slate-400">University of Innaloo</span>
              <div className="h-[2px] bg-slate-300 flex-1"></div>
           </div>
           <div className="bg-[#F2EFE9] border-2 border-slate-900 rounded-lg p-6 md:p-8 flex flex-col md:flex-row gap-6 items-start shadow-sm">
              <div className="shrink-0 mx-auto md:mx-0">
                 <div className="w-24 h-24 rounded-full border-2 border-slate-900 overflow-hidden bg-white shadow-sm">
                    <img src="/images/professor.png" alt="Professor Remy" className="w-full h-full object-cover"/>
                 </div>
                 <p className="text-center text-[10px] font-bold uppercase tracking-widest mt-2 text-slate-500">Prof. Remy</p>
              </div>
              <div className="flex-1 text-center md:text-left">
                 <h3 className="text-xl font-bold text-slate-900 mb-2 font-serif">{issueData.professor.title}</h3>
                 <p className="text-md text-slate-700 leading-relaxed font-serif italic">"{issueData.professor.content}"</p>
              </div>
           </div>
        </section>

        {/* --- THE MYSTIC BUTTON (Replaces the error-causing text) --- */}
        <section className="max-w-4xl mx-auto mb-20 text-center">
           <div className="relative group cursor-pointer inline-block">
             <Link href="/mystic">
               <div className="w-full max-w-sm mx-auto transform transition-transform duration-300 group-hover:scale-105">
                 <img src="/images/mystic_link.png" alt="Enter the Mystic's Tent" className="rounded-full border-4 border-slate-900 shadow-xl"/>
                 <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 bg-purple-900 text-orange-100 px-6 py-2 rounded-full border-2 border-orange-400 shadow-lg whitespace-nowrap">
                    <span className="font-bold uppercase tracking-widest text-xs">Consult The Stars</span>
                 </div>
               </div>
             </Link>
           </div>
        </section>

        {/* --- THE BARKER CLASSIFIEDS --- */}
        <section className="max-w-4xl mx-auto border-t-4 border-double border-slate-300 pt-12">
            <div className="flex flex-col md:flex-row items-center justify-center gap-6 mb-10">
                <div className="w-20 h-20 rounded-full border-2 border-slate-900 overflow-hidden bg-white shadow-sm shrink-0">
                    <img src="/images/newsboy.png" alt="The Barker" className="w-full h-full object-cover"/>
                </div>
                <h3 className="text-center text-3xl font-black uppercase text-slate-900 tracking-tighter">The Barker Classifieds</h3>
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