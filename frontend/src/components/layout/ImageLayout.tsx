import React from 'react';
import { Box } from '@mui/material';

interface ImageLayoutProps {
  children: React.ReactNode;
}

const ImageLayout: React.FC<ImageLayoutProps> = ({ children }) => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        width: '100vw',
        background: 'linear-gradient(135deg, #2E1437 0%, #1B998B 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 3,
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: `
            radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 20%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 20%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 30c4-8 8-4 12 0 4 4 8 8 12 0-4 8-8 4-12 0-4-4-8-8-12 0z' fill='rgba(255,255,255,0.05)' /%3E%3C/svg%3E")
          `,
          pointerEvents: 'none',
        },
      }}
    >
      {children}
    </Box>
  );
};

export default ImageLayout; 