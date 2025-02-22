import React from 'react';
import { Box } from '@mui/material';

interface MainProps {
  children?: React.ReactNode;
}

const Main: React.FC<MainProps> = ({ children }) => {
  return (
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        height: '100vh',
        overflow: 'auto',
        position: 'relative',
      }}
    >
      {children}
    </Box>
  );
};

// Export without any SSR/SSG methods
export default Main;
