'use client';

import { useState, useEffect } from 'react';

export default function SocialBar({ id, title }: { id: string; title: string }) {
  const [likes, setLikes] = useState(0);
  const [hasLiked, setHasLiked] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    // Load local "fake" stats
    const stored = localStorage.getItem(`like-${id}`);
    if (stored) setHasLiked(true);
    // Randomize initial "global" likes for social proof illusion
    setLikes(Math.floor(Math.random() * 50) + 10);
  }, [id]);

  const handleLike = () => {
    if (hasLiked) {
      setLikes((prev) => prev - 1);
      setHasLiked(false);
      localStorage.removeItem(`like-${id}`);
    } else {
      setLikes((prev) => prev + 1);
      setHasLiked(true);
      localStorage.setItem(`like-${id}`, 'true');
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'The Remy Digest',
          text: title,
          url: window.location.href,
        });
      } catch (err) {
        console.log('Share canceled');
      }
    } else {
      // Fallback for Desktop: Copy URL
      navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="flex items-center gap-4 py-6 border-t border-b border-current opacity-80 my-8">
      
      {/* LIKE BUTTON */}
      <button 
        onClick={handleLike}
        className={`flex items-center gap-2 px-4 py-2 rounded-full transition-all border border-current hover:bg-black/10
          ${hasLiked ? 'font-bold text-red-600' : ''}`}
      >
        <span className="text-xl">{hasLiked ? '❤️' : '♡'}</span>
        <span>{likes} {hasLiked ? 'Liked' : 'Like'}</span>
      </button>

      {/* SHARE BUTTON */}
      <button 
        onClick={handleShare}
        className="flex items-center gap-2 px-4 py-2 rounded-full border border-current hover:bg-black/10 transition-all"
      >
        <span className="text-xl">📤</span>
        <span>{copied ? 'Copied Link!' : 'Share'}</span>
      </button>

    </div>
  );
}