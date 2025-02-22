import React from 'react';

interface ImageLayoutProps {
  children: React.ReactNode;
}

const ImageLayout: React.FC<ImageLayoutProps> = ({ children }) => {
  return (
    <div className="relative min-h-screen w-screen flex items-center justify-center p-3 bg-gradient-to-br from-[#2E1437] to-[#1B998B]">
      {/* Background Overlay */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage: `
            radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 20%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 20%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 30c4-8 8-4 12 0 4 4 8 8 12 0-4 8-8 4-12 0-4-4-8-8-12 0z' fill='rgba(255,255,255,0.05)' /%3E%3C/svg%3E")
          `,
        }}
      ></div>
      
      {children}
    </div>
  );
};

export default ImageLayout;
