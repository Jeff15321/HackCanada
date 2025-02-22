import React from 'react';

interface MainProps {
  children?: React.ReactNode;
}

const Main: React.FC<MainProps> = ({ children }) => {
  return (
    <main className="min-h-screen w-full bg-black overflow-y-auto scrollbar-hide">
      {children}
    </main>
  );
};

// Export without any SSR/SSG methods
export default Main;
