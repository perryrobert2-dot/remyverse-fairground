import React from 'react';
import issueData from "./data/current_issue.json";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#FDFBF7] text-slate-800 font-sans selection:bg-orange-200 pb-20">
      
      {/* --- HEADER --- */}
      <nav className="border-b-2 border-slate-900 bg-white py-6">
        <div className="max-w-4xl mx-auto px-6 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-black tracking-tighter text-slate-900 uppercase">
              The Remy Digest
            </h1>
            <p className="text-xs font-bold tracking-widest text-slate-500 mt-1">
              THE NORTHERN BEACHES' ONLY RELIABLE SOURCE
            </p>
          </div>
          <div className="text-right hidden sm:block">
            <p className="text-sm font-semibold">{issueData.date}</p>
            <p className="text-xs text-slate-400 uppercase tracking-widest">Issue #{issueData.issueNumber}</p>
          </div>
        </div>
      </nav>

      {/* --- MAIN STAGE --- */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        
        {/* HERO IMAGE */}
        <section className="shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] border-2 border-slate-900 rounded-lg overflow-hidden bg-white mb-12">
           <img 
             src={issueData.imagePath} 
             alt={issueData.headline} 
             className="w-full h-auto object-cover"
           />
        </section>

        {/* HEADLINE SECTION */}
        <article className="max-w-2xl mx-auto text-center mb-16">
          <span className="inline-block bg-slate-900 text-white text-xs font-bold px-3 py-1 mb-4 rounded-full uppercase tracking-wider">
            {issueData.category}
          </span>
          <h2 className="text-4xl md:text-5xl font-black text-slate-900 mb-6 leading-tight">
            {issueData.headline}
          </h2>
          <p className="text-xl md:text-2xl text-slate-600 font-serif italic leading-relaxed">
            "{issueData.subtext}"
          </p>
        </article>

        {/* --- THE PROFESSOR'S CORNER --- */}
        <section className="max-w-2xl mx-auto bg-[#F2EFE9] border-l-4 border-slate-400 p-8 rounded-r-lg">
           <div className="flex items-start gap-4">
              <div className="flex-1">
                 <h3 className="text-sm font-bold uppercase tracking-widest text-slate-500 mb-2">
                    {issueData.professor.title}
                 </h3>
                 <p className="text-lg font-serif text-slate-800 leading-relaxed">
                    {issueData.professor.content}
                 </p>
              </div>
           </div>
        </section>

      </div>
    </main>
  );
}