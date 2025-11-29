'use client';
import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';

const clean = (text: string, maxLength: number = 0) => {
  if (!text) return "";
  let cleaned = text.replace(/[*_#]/g, '').replace(/^(Headline|Title|Teaser|Body|Description|Exhibit|Rating|Topic|Letter):/i, '').replace(/^["']+|["']+$/g, '').trim();
  if (maxLength > 0 && cleaned.length > maxLength) cleaned = cleaned.substring(0, maxLength) + "...";
  return cleaned;
};

export default function Home() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { fetch('/data/current_issue.json').then((res) => res.json()).then((data) => setData(data)); }, []);
  if (!data) return <div className="min-h-screen bg-[#8b1c1c] p-20 text-center font-mono text-[#f4e4bc] animate-pulse">Waiting for the Night Shift...</div>;

  const editorial = data.editorial || { title: "Loading...", teaser: "..." };
  const arts = data.arts || { title: "Loading...", rating: "?" };
  const pitd = data.pitd || { title: "Under Construction" };
  const blotter = data.blotter || { incident: "Quiet Night" };
  const advice = data.advice || { main_q: "..." };
  
  // ROBUST TEASER LOGIC
  const firstLetter = data.letters?.[0] || {};
  // Prefer body, fallback to topic, fallback to default
  const mailTeaser = firstLetter.body ? firstLetter.body : (firstLetter.topic || "Check the mailbag for local complaints.");

  return (
    <main className="min-h-screen bg-[#8b1c1c] p-4 md:p-8 font-sans selection:bg-yellow-300">
      <header className="max-w-7xl mx-auto text-center mb-8 text-[#f4e4bc]">
        <h1 className="text-5xl md:text-8xl font-black uppercase tracking-tighter leading-none drop-shadow-xl hover:scale-[1.01] transition-transform cursor-default">The Remy Digest</h1>
        <div className="border-t-4 border-b-4 border-[#f4e4bc] py-2 mt-4 flex justify-between items-center px-4 font-mono text-sm uppercase font-bold tracking-widest">
           <span>Vol. {data.meta?.version}</span>
           <span className="hidden md:inline">"News That Sniffs Out The Truth"</span>
           <span>{new Date(data.meta?.generated_at).toLocaleDateString()}</span>
        </div>
      </header>

      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6">

        {/* EDITORIAL */}
        <Link href="/editorial" className="md:col-span-2 group">
            <article className="bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,0.5)] border-4 border-black h-[500px] flex flex-col group-hover:-translate-y-2 transition-transform relative overflow-hidden">
                <div className="h-64 relative bg-slate-200 border-b-4 border-black"><Image src="/personas/professor.png" alt="Editor" fill className="object-contain p-2" /></div>
                <div className="p-6 flex flex-col flex-1">
                    <h2 className="text-2xl font-black leading-tight mb-2 text-black group-hover:text-red-700 transition-colors line-clamp-3">{clean(editorial.title)}</h2>
                    <p className="font-serif text-sm text-black line-clamp-3">{clean(editorial.teaser)}</p>
                </div>
            </article>
        </Link>
        
        {/* ARTS */}
        <Link href="/arts" className="group">
            <article className="bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,0.5)] border-4 border-black h-[500px] flex flex-col group-hover:-translate-y-2 transition-transform">
                <div className="h-48 relative bg-slate-100 border-b-4 border-black"><Image src="/personas/critic.png" alt="Critic" fill className="object-contain p-2" /></div>
                <div className="p-5 flex flex-col flex-1">
                    <span className="text-xs font-black text-black uppercase">Arts Review</span>
                    <h3 className="text-lg font-black leading-tight mb-2 text-black group-hover:text-red-700 line-clamp-3">{clean(arts.title)}</h3>
                    <div className="mt-auto self-start bg-black text-white px-2 py-1 text-xs font-bold">{clean(arts.rating)}</div>
                </div>
            </article>
        </Link>
        
        {/* PITD */}
        <Link href="/pitd" className="group">
            <article className="bg-[#f0d05c] shadow-[8px_8px_0px_0px_rgba(0,0,0,0.5)] border-4 border-black p-5 h-[500px] flex flex-col group-hover:-translate-y-2 transition-transform text-center justify-center">
                <div className="w-20 h-20 bg-white rounded-full border-4 border-black mx-auto mb-4 relative"><Image src="/personas/critic.png" alt="Fight" fill className="object-cover rounded-full" /></div>
                <h3 className="font-black text-xl uppercase italic text-black mb-2">Throw Down</h3>
                <p className="font-black text-lg leading-tight transform -rotate-1 group-hover:rotate-0 transition-transform line-clamp-4 text-black">{clean(pitd.title)}</p>
            </article>
        </Link>

        {/* LETTERS */}
        <Link href="/letters" className="group">
            <div className="bg-[#f0e6d2] shadow-[8px_8px_0px_0px_rgba(0,0,0,0.5)] border-4 border-black p-5 h-64 flex flex-col group-hover:-rotate-1 transition-transform relative overflow-hidden">
                 <div className="absolute top-0 right-0 w-16 h-16 bg-red-600 text-white flex items-center justify-center font-black text-xs rotate-45 translate-x-6 -translate-y-6 shadow-md">NEW</div>
                 <div className="flex items-center gap-3 mb-3"><div className="w-10 h-10 relative rounded-full border-2 border-black bg-white overflow-hidden"><Image src="/personas/mail_carrier.jpg" alt="Mail" fill className="object-cover" /></div><h3 className="font-black text-lg uppercase underline decoration-wavy text-black">Mailbag</h3></div>
                 
                 {/* DYNAMIC TEASER */}
                 <p className="text-sm font-serif italic text-black line-clamp-3">"{clean(mailTeaser, 100)}"</p>
                 
                 <div className="mt-auto text-xs font-bold text-red-700 uppercase">Read Letters →</div>
            </div>
        </Link>

        {/* CLASSIFIEDS */}
        <Link href="/classifieds" className="group">
            <div className="bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,0.5)] border-4 border-black p-5 h-64 flex flex-col group-hover:-translate-y-1 transition-transform">
                 <div className="flex justify-between items-center mb-2 border-b-2 border-black pb-1"><span className="font-black uppercase text-sm flex items-center gap-1 text-black">🚨 Blotter</span><span className="text-red-600 text-[10px] font-bold animate-pulse">LIVE</span></div>
                 <h4 className="font-bold text-md mb-1 line-clamp-1 leading-tight text-black">{clean(blotter.incident)}</h4>
                 <p className="text-xs text-black leading-snug line-clamp-3 font-mono">"{clean(blotter.details)}"</p>
                 <div className="mt-auto text-xs font-bold text-black uppercase text-right group-hover:text-red-700">All Ads →</div>
            </div>
        </Link>

        {/* ADVICE */}
        <Link href="/advice" className="group">
            <div className="bg-[#e8f4bc] shadow-[8px_8px_0px_0px_rgba(0,0,0,0.5)] border-4 border-black p-5 h-64 flex flex-col group-hover:-rotate-1 transition-transform">
                <div className="flex items-center gap-3 mb-3"><div className="w-10 h-10 relative rounded-full border-2 border-black bg-white overflow-hidden"><Image src="/personas/aunt.png" alt="Aunt" fill className="object-cover" /></div><h3 className="font-black text-lg uppercase text-black">Ask Auntie</h3></div>
                <div className="font-bold text-sm leading-tight line-clamp-3 text-black">"{clean(advice.main_q)}"</div>
            </div>
        </Link>

        <Link href="/horoscopes" className="group">
            <div className="bg-slate-900 text-white shadow-[8px_8px_0px_0px_rgba(255,255,255,0.1)] border-4 border-purple-500 p-4 h-64 flex flex-col group-hover:-translate-y-1 transition-transform">
                 <div className="flex items-center justify-between mb-2 border-b border-slate-700 pb-1"><h3 className="font-black text-sm text-purple-300 tracking-widest">STARS</h3><Image src="/personas/mystic.png" width={24} height={24} alt="Mystic" className="rounded-full ring-2 ring-purple-500" /></div>
                 <div className="space-y-2 opacity-80">{data.horoscopes?.slice(0, 2).map((h: any) => (<div key={h.sign} className="flex gap-2 text-xs"><div><span className="font-bold text-purple-300 uppercase block text-[10px]">{h.sign}</span><span className="leading-tight text-[10px] line-clamp-1">{clean(h.prediction)}</span></div></div>))}</div>
            </div>
        </Link>

      </div>
    </main>
  );
}