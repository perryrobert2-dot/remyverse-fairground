'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import SocialBar from '@/components/SocialBar';

export default function PITDPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { fetch('/data/current_issue.json').then(r => r.json()).then(setData); }, []);
  if (!data) return <div className="p-20 text-center bg-[#f0d05c]">Loading...</div>;

  const pitd = data.pitd || {};

  return (
    <main className="min-h-screen bg-[#f0d05c] flex flex-col items-center justify-center p-6 text-center font-sans">
      <Link href="/" className="absolute top-6 left-6 font-black uppercase tracking-widest text-xs border-2 border-black px-4 py-2 hover:bg-black hover:text-white transition-colors">← Escape</Link>
      
      <div className="max-w-4xl w-full border-8 border-black bg-white p-8 md:p-16 shadow-[20px_20px_0px_0px_rgba(0,0,0,1)] relative">
         <div className="absolute -top-6 left-1/2 -translate-x-1/2 bg-black text-white px-6 py-2 font-black uppercase tracking-widest text-sm rotate-1">
            Current Installation
         </div>

         {/* SIZED DOWN TO 2XL */}
         <span className="block text-red-600 font-black uppercase tracking-[0.3em] mb-4 text-xl md:text-2xl animate-pulse">
            Exhibit A
         </span>
         
         {/* SIZED DOWN TO 5XL */}
         <h1 className="text-3xl md:text-5xl font-black text-black mb-8 leading-none uppercase italic transform -rotate-1">
            {pitd.title}
         </h1>
         
         <div className="w-24 h-2 bg-black mx-auto mb-8"></div>
         
         <p className="font-mono text-lg md:text-xl text-slate-800 leading-relaxed max-w-2xl mx-auto whitespace-pre-line">
            {pitd.description}
         </p>

         <div className="mt-12 pt-8 border-t-4 border-black border-dashed">
            <SocialBar id="pitd-exhibit" title={pitd.title} />
         </div>
      </div>
    </main>
  );
}