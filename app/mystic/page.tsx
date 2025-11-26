import React from 'react';
import Link from 'next/link';
import issueData from "../data/current_issue.json";

// ---------------------------------------------------------
// 🔧 CONFIGURATION
const BUCKET_URL = "https://storage.googleapis.com/remys-digest-public-assets/";
// ---------------------------------------------------------

export default function MysticTent() {
  return (
    <main className="min-h-screen bg-slate-900 text-orange-100 font-sans pb-20">
      
      {/* NAVIGATION */}
      <nav className="p-6">
        <Link href="/" className="text-orange-300 hover:text-white uppercase tracking-widest text-xs font-bold">
          ← Back to Fairground
        </Link>
      </nav>

      {/* HEADER */}
      <header className="text-center mb-16">
        <h1 className="text-5xl md:text-7xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-orange-400 mb-4 tracking-tighter">
          The Mystic's Tent
        </h1>
        <p className="text-purple-300 font-serif italic text-xl">
          "The stars do not lie, but they often exaggerate."
        </p>
      </header>

      {/* THE ZODIAC GRID */}
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          
          {issueData.mystic && Array.isArray(issueData.mystic) ? (
            issueData.mystic.map((item, index) => {
              // Convert "Aries" to "aries.png"
              const imageFilename = `${item.sign.toLowerCase()}.png`;
              const imageUrl = `${BUCKET_URL}${imageFilename}`;

              return (
                <div key={index} className="bg-slate-800 border border-slate-700 p-8 rounded-2xl hover:border-orange-500/50 transition-all shadow-lg hover:shadow-orange-500/10 group flex flex-col items-center text-center">
                  
                  {/* ZODIAC IMAGE FROM BUCKET */}
                  <div className="w-32 h-32 mb-6 relative p-4 bg-slate-900/50 rounded-full border border-slate-700 group-hover:border-orange-500/30 transition-colors">
                    <img 
                      src={imageUrl} 
                      alt={item.sign}
                      className="w-full h-full object-contain opacity-90 group-hover:opacity-100 transition-opacity drop-shadow-[0_0_15px_rgba(168,85,247,0.3)]"
                    />
                  </div>

                  <h3 className="text-2xl font-black text-white mb-4 uppercase tracking-wider group-hover:text-orange-400 transition-colors">
                    {item.sign}
                  </h3>
                  <p className="font-serif text-lg text-slate-300 leading-relaxed italic">
                    "{item.prediction}"
                  </p>
                </div>
              );
            })
          ) : (
            <div className="col-span-full text-center text-slate-500">
              The Mystic is currently on a tea break. (Run the generator to fill the stars)
            </div>
          )}

        </div>
      </div>

    </main>
  );
}