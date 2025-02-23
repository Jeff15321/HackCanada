import React from 'react';

interface BackgroundWrapperProps {
  children: React.ReactNode;
}

const BackgroundWrapper: React.FC<BackgroundWrapperProps> = ({ children }) => {
  return (
    <div className="min-h-screen relative bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] 
      from-purple-900/20 via-black to-black">
      {/* Ambient background effects */}
      <div className="fixed inset-0 pointer-events-none">
        {/* Base grid pattern - thick but less dense */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(6,182,212,0.3)_2px,transparent_2px),linear-gradient(to_bottom,rgba(6,182,212,0.3)_2px,transparent_2px)] 
          bg-[size:1.5rem_1.5rem]" />
        
        {/* Smaller grid pattern - less dense */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(6,182,212,0.15)_1px,transparent_1px),linear-gradient(to_bottom,rgba(6,182,212,0.15)_1px,transparent_1px)] 
          bg-[size:0.5rem_0.5rem]" />

        {/* Diagonal grid lines - slightly more spaced */}
        <div className="absolute inset-0 bg-[repeating-linear-gradient(45deg,rgba(6,182,212,0.1)_0px,rgba(6,182,212,0.1)_3px,transparent_3px,transparent_8px)]" />
        
        {/* Glowing orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl animate-pulse" />
        
        {/* Scanlines - slightly less dense */}
        <div className="absolute inset-0 bg-[repeating-linear-gradient(0deg,rgba(6,182,212,0.1)_0px,rgba(6,182,212,0.1)_2px,transparent_2px,transparent_3px)]" />
        
        {/* Gradient overlays */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-black/30" />
        <div className="absolute inset-0 bg-gradient-to-r from-black/10 via-transparent to-black/10" />
      </div>

      {/* Content */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
};

export default BackgroundWrapper; 