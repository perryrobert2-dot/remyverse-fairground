'use client';
import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import SocialBar from '@/components/SocialBar';

export default function EditorialPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { fetch('/data/current_issue.json').then(r => r.json()).then(setData); }, []);
  if (!data) return <div className="p-20 text-center font-serif text-black">Loading the press...</div>;

  const editorial = data.editorial || {};

  return (
    <main className="min-h-screen bg-[#fcfbf9] text-black p-6 md:p-12 font-serif selection:bg-red-200">
      
      <nav className="mb-12 border-b-2 border-black pb-4 flex justify-between items-end">
        <Link href="/" className="font-sans text-xs font-bold uppercase tracking-widest hover:text-red-700 transition-colors text-black">← Front Page</Link>
        <div className="text-right">
             <h1 className="font-black text-3xl md:text-5xl uppercase tracking-tighter leading-none text-black">The Editorial</h1>
             <span className="font-sans text-xs font-bold uppercase tracking-widest text-slate-500">Est. 2024 • Cromer, NSW</span>
        </div>
      </nav>

      {/* SINGLE COLUMN LAYOUT */}
      <article className="max-w-3xl mx-auto">
            <span className="font-sans text-xs font-bold uppercase tracking-widest text-red-700 mb-2 block text-center">From The Desk Of Professor Remy</span>
            
            {/* HEADLINE: CENTERED */}
            <h2 className="text-3xl md:text-5xl font-black leading-tight mb-8 capitalize text-center text-black">
                {editorial.title}
            </h2>
            
            <div className="mb-8 w-full relative aspect-video border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,0.2)]">
                <Image src="/personas/professor.png" alt="Professor" fill className="object-cover object-top" />
            </div>

            {/* BODY: LEFT ALIGNED & FIXED SIZE & BLACK */}
            <div className="text-base md:text-lg leading-relaxed text-black whitespace-pre-line text-left max-w-prose mx-auto">
                <p className="font-bold mb-4 text-black text-lg border-l-4 border-red-700 pl-4">
                    {editorial.teaser}
                </p>
                {editorial.body}
            </div>
            
            <div className="mt-12 pt-8 border-t border-slate-200 flex justify-center">
                <SocialBar id="editorial" title={editorial.title} />
            </div>
      </article>
    </main>
  );
}