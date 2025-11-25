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
        <article className="max-w-2xl mx-auto text-center mb-12">
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

        {/* --- MAIN ARTICLE BODY --- */}
        <article className="max-w-2xl mx-auto mb-16 font-serif text-lg leading-relaxed text-slate-800">
           {issueData.body && issueData.body.split('\n').map((paragraph, index) => (
             paragraph.trim() !== "" && (
               <p key={index} className="mb-6">
                 {paragraph}
               </p>
             )
           ))}
           <div className="flex justify-center mt-8">
             <span className="text-slate-400 tracking-widest text-xs uppercase">*** End of Report ***</span>
           </div>
        </article>

        {/* --- THE PROFESSOR'S CORNER --- */}
        <section className="max-w-2xl mx-auto mt-16 mb-20">
           <div className="flex items-center gap-3 mb-4">
              <div className="h-[2px] bg-slate-300 flex-1"></div>
              <span className="text-xs font-bold uppercase tracking-widest text-slate-400">From The Archives</span>
              <div className="h-[2px] bg-slate-300 flex-1"></div>
           </div>

           <div className="bg-[#F2EFE9] border-2 border-slate-900 rounded-lg p-6 md:p-8 flex flex-col md:flex-row gap-6 items-start shadow-[6px_6px_0px_0px_rgba(0,0,0,0.1)]">
              <div className="shrink-0 mx-auto md:mx-0">
                 <div className="w-24 h-24 rounded-full border-2 border-slate-900 overflow-hidden bg-white shadow-sm">
                    {/* Ensure professor.png exists in /public/images/ */}
                    <img 
                       src="/images/professor.png" 
                       alt="Professor Remy" 
                       className="w-full h-full object-cover"
                    />
                 </div>
                 <p className="text-center text-[10px] font-bold uppercase tracking-widest mt-2 text-slate-500">
                    Prof. Remy
                 </p>
              </div>

              <div className="flex-1 text-center md:text-left">
                 <h3 className="text-xl font-bold text-slate-900 mb-2 font-serif">
                    {issueData.professor.title}
                 </h3>
                 <p className="text-md text-slate-700 leading-relaxed font-serif italic">
                    "{issueData.professor.content}"
                 </p>
              </div>
           </div>
        </section>

        {/* --- THE BARKER (CLASSIFIEDS) --- */}
        <section className="max-w-4xl mx-auto border-t-4 border-double border-slate-300 pt-12">
            <h3 className="text-center text-3xl font-black uppercase text-slate-900 mb-8 tracking-tighter">
                The Barker Classifieds
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Safe check: if classifieds exist, map them. If not, show nothing. */}
                {issueData.classifieds && issueData.classifieds.map((ad, index) => (
                    <div key={index} className="bg-white border border-slate-200 p-4 shadow-sm hover:shadow-md transition-shadow">
                        <p className="font-mono text-xs text-slate-400 mb-2 uppercase tracking-widest">
                            Ad Ref: #{1000 + index}
                        </p>
                        <p className="font-serif text-sm leading-relaxed text-slate-800">
                            {ad}
                        </p>
                    </div>
                ))}
            </div>
        </section>

      </div>
    </main>
  );
}