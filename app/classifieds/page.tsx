'use client';
import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import SocialBar from '@/components/SocialBar';

export default function ClassifiedsPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { fetch('/data/current_issue.json').then(r => r.json()).then(setData); }, []);
  if (!data) return <div className="p-20 text-center bg-[#d4c4a8] text-black">Loading...</div>;

  const blotter = data.blotter || {};
  const adsRaw = data.ads || {};

  // Simple ad parser
  const getAd = (n: number, type: string, color: string) => ({
      type: adsRaw[`ad${n}_type`] || type,
      title: adsRaw[`ad${n}_title`] || "Space Available",
      body: adsRaw[`ad${n}_body`] || "Contact Bazza.",
      color
  });

  const ads = [getAd(1, "LOST", "bg-white"), getAd(2, "SALE", "bg-yellow-100"), getAd(3, "WANTED", "bg-blue-100")];

  return (
    <main className="min-h-screen bg-[#b5a68e] font-sans text-black relative overflow-hidden">
      <div className="absolute inset-0 opacity-10 pointer-events-none" style={{ backgroundImage: 'radial-gradient(#000 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
      <nav className="p-4 border-b-4 border-black mb-8 flex justify-between items-center bg-[#a39276] relative z-10 shadow-lg">
        <Link href="/" className="font-black uppercase hover:text-white">← Back</Link>
        <div className="font-mono text-xs uppercase tracking-widest font-bold">Community Board</div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 pb-20 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
            {/* BLOTTER */}
            <div className="md:col-span-2 bg-white p-8 shadow-lg transform rotate-1 relative">
                <div className="flex items-center gap-4 mb-6 border-b-4 border-black pb-4">
                    <div className="w-20 h-20 relative grayscale contrast-125"><Image src="/personas/critic.png" alt="Police" fill className="object-cover" /></div>
                    <div><h2 className="text-3xl font-black uppercase leading-none">Police Blotter</h2></div>
                </div>
                {/* Added 'capitalize' class */}
                <h3 className="text-2xl font-bold mb-2 capitalize">{blotter.incident}</h3>
                <div className="bg-black text-white px-2 py-0.5 text-xs font-bold uppercase rounded inline-block mb-4">LOC: {blotter.location}</div>
                
                {/* FORCED LOWERCASE with normal-case class */}
                <p className="font-serif text-xl leading-relaxed mb-8 normal-case first-letter:uppercase">
                    {blotter.details}
                </p>
                
                <div className="opacity-80 scale-90 origin-left"><SocialBar id="blotter" title="Crime Report" /></div>
            </div>

            {/* ADS */}
            <div className="space-y-6">
                {ads.map((ad, i) => (
                    <div key={i} className={`${ad.color} p-4 shadow-lg transform hover:scale-105 transition-transform duration-300 relative text-black`} style={{ rotate: `${(i%2===0?1:-1)*(Math.random()*3+1)}deg` }}>
                         <div className="absolute -top-2 left-1/2 w-3 h-3 rounded-full bg-blue-800 shadow-sm"></div>
                         <div className="font-black text-xs opacity-50 uppercase mb-1 tracking-widest">{ad.type}</div>
                         <h4 className="font-bold text-lg leading-tight mb-2 capitalize">{ad.title}</h4>
                         <p className="font-serif text-sm leading-snug normal-case">{ad.body}</p>
                    </div>
                ))}
            </div>
        </div>
      </div>
    </main>
  );
}