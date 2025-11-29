'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import SocialBar from '@/components/SocialBar'; // Assumes SocialBar component exists

export default function ArtsPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { fetch('/data/current_issue.json').then(r => r.json()).then(setData); }, []);
  if (!data) return <div className="p-20 text-center bg-[#1a1a1a] text-white">Loading...</div>;

  const arts = data.arts || {};

  return (
    <main className="min-h-screen bg-[#1a1a1a] text-gray-200 font-sans selection:bg-amber-500 selection:text-black">
      <nav className="p-4 border-b border-gray-700 mb-8 flex justify-between items-center text-gray-400">
        <Link href="/" className="font-bold uppercase hover:text-white transition-colors">← Exit Gallery</Link>
        <div className="font-mono text-xs uppercase tracking-widest text-amber-500">The White Cube</div>
      </nav>

      <div className="max-w-3xl mx-auto px-6">
        <div className="mb-12 text-center">
             <span className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-4 block">Critical Review</span>
             <h1 className="text-3xl md:text-5xl font-serif text-amber-50 leading-tight mb-8 capitalize">
                {arts.title}
             </h1>
             <div className="inline-flex items-center gap-3 border border-gray-700 px-6 py-3 rounded-full">
                <span className="text-xs font-bold uppercase tracking-widest text-amber-500">Verdict</span>
                <span className="w-px h-4 bg-gray-700"></span>
                <span className="text-lg font-black text-white">{arts.rating}</span>
            </div>
        </div>
        
        <div className="font-serif text-lg md:text-xl leading-relaxed text-gray-300 space-y-6 whitespace-pre-line text-justify max-w-prose mx-auto">
            <p className="font-bold text-amber-50/80 border-l-2 border-amber-500 pl-4">{arts.teaser}</p>
            {arts.body}
        </div>
        
        {/* RESTORED SOCIAL LINKS */}
        <div className="opacity-70 mt-16 pt-8 border-t border-gray-800 flex justify-center">
             <SocialBar id="arts-review" title={arts.title} />
        </div>
      </div>
    </main>
  );
}