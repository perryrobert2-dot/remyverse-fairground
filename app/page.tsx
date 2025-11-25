import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center bg-[#fdfbf7] text-black font-sans">
      
      {/* HEADER SECTION */}
      <div className="w-full max-w-5xl mt-10 px-4">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold font-serif tracking-tight mb-2">The Remy Digest</h1>
          <p className="text-gray-600 italic">The Northern Beaches' Only Reliable Source</p>
        </div>
        
        {/* THE FACTORY IMAGE */}
        <div className="w-full shadow-2xl border-4 border-black overflow-hidden rounded-lg">
           <Image 
             src="/daily_digest_widescreen.jpg" 
             alt="Daily Digest Header"
             width={1920}
             height={1080}
             className="w-full h-auto object-cover"
             priority
           />
        </div>
      </div>

      {/* BODY CONTENT */}
      <div className="max-w-3xl mt-12 p-6 bg-white shadow-lg border-2 border-gray-100 rounded-sm">
        
        {/* SECTION 1: THE LECTURE HALL (The Professor) */}
        <section className="mb-10 border-b-2 border-gray-200 pb-8">
          <h2 className="font-bold text-3xl font-serif mb-2 text-gray-900">The Editor's Desk</h2>
          <p className="text-gray-500 italic mb-4 text-sm">By Professor Remy</p>
          
          <p className="mb-4 leading-relaxed">
            One observes with considerable interest the remarkable engineering principles 
            embedded within the structure of a bird's nest. It is a testament to natural 
            architectural ingenuity that puts our own Council's zoning laws to shame.
          </p>
          
          <div className="bg-yellow-50 p-4 border-l-4 border-yellow-400 my-6">
            <h3 className="font-bold text-lg text-yellow-800">💡 Remarkable Find</h3>
            <p className="italic text-gray-700">
              The octopus possesses three hearts: two pump blood through its gills, while 
              the third circulates blood to the rest of its body. A redundancy our local 
              hospital could certainly aspire to.
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg text-center">
             <span className="block text-xs font-bold uppercase tracking-widest text-gray-400">Word of the Day</span>
             <strong className="text-2xl text-indigo-900">Verisimilitude</strong>
             <p className="text-gray-600 mt-1">The appearance or semblance of being true or real.</p>
          </div>
        </section>

        {/* SECTION 2: THE ODDITORIUM (The Barker) */}
        <section className="mb-10">
          <div className="flex items-center mb-4">
             <span className="text-2xl mr-2">🎪</span>
             <h2 className="font-bold text-2xl font-serif text-red-800">The Odditorium: Epic Fails</h2>
          </div>
          
          <h3 className="font-bold text-xl mb-2">The U.S. Camel Corps</h3>
          <p className="mb-4 leading-relaxed text-gray-800">
            In the 1850s, the U.S. Army imported dozens of dromedary camels to serve as pack animals 
            in the American Southwest. Regrettably, these creatures frequently unnerved horses 
            and mules, culminating in the corps' dissolution.
          </p>
          <p className="leading-relaxed text-gray-800">
            Much like the recent proposal to replace the Manly Ferry with a monorail, it was 
            a fascinating, albeit ultimately impractical, experiment.
          </p>
        </section>

        {/* SECTION 3: THE MYSTIC (Horoscopes) */}
        <section className="bg-indigo-900 text-white p-6 rounded-xl relative overflow-hidden">
          <h2 className="font-bold text-2xl font-serif mb-4 relative z-10">🔮 Daily Horoscopes</h2>
          <p className="text-indigo-200 italic mb-6 relative z-10">Channeled by the spirits of the literary greats.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 relative z-10">
            <div className="bg-indigo-800 p-3 rounded">
              <strong className="text-yellow-400 block">Aries</strong>
              <span className="text-sm">The universe places a whimsical clue in the mundane. Watch where you step.</span>
            </div>
            <div className="bg-indigo-800 p-3 rounded">
              <strong className="text-yellow-400 block">Taurus</strong>
              <span className="text-sm">One must find beauty in unexpected places. Even the Warringah Mall car park.</span>
            </div>
          </div>
        </section>

      </div>
    </main>
  );
}