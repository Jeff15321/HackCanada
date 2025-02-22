import React, { useState, useRef } from 'react';
import { Box, Button, IconButton, Typography, Paper } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { useImage } from '../../contexts/ImageContext';

interface ImageDropProps {
  onSubmit: () => void;
}

const ImageDrop: React.FC<ImageDropProps> = ({ onSubmit }) => {
  const [image, setImage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { setSelectedFile, setImageUrl } = useImage();

  const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      console.log("Dropped file:", file);
      handleImageSelect(file);
    }
  };

  const handleImageSelect = (file: File) => {
    console.log("Selected file in handleImageSelect:", file);
    setSelectedFile(file);
    if (file) {
      const url = URL.createObjectURL(file);
      setImageUrl(url);
      console.log("Created URL:", url);
    }

    const reader = new FileReader();
    reader.onload = () => {
      setImage(reader.result as string);
      console.log("Image set to:", file);
    };
    reader.readAsDataURL(file);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      console.log("File input file:", file);
      handleImageSelect(file);
    }
  };

  const clearImage = () => {
    setImage(null);
    setSelectedFile(null);
    setImageUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <Paper
      elevation={24}
      sx={{
        width: '100%',
        maxWidth: 1200,
        borderRadius: 4,
        overflow: 'hidden',
        background: 'rgba(255, 255, 255, 0.9)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(45deg, rgba(27, 153, 139, 0.1) 0%, rgba(46, 20, 55, 0.1) 100%)',
          pointerEvents: 'none',
        }
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          minHeight: 500,
        }}
      >
        {/* Left Side - Drop Zone */}
        <Box
          sx={{
            flex: '2',
            p: 4,
            borderRight: { xs: 'none', md: '1px solid rgba(46, 20, 55, 0.1)' },
            borderBottom: { xs: '1px solid rgba(46, 20, 55, 0.1)', md: 'none' },
          }}
        >
          <Box
            sx={{
              width: '100%',
              height: '100%',
              border: '3px dashed',
              borderColor: image ? '#1B998B' : 'rgba(46, 20, 55, 0.2)',
              borderRadius: 3,
              transition: 'all 0.3s ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              position: 'relative',
              overflow: 'hidden',
              background: 'rgba(255, 255, 255, 0.5)',
              '&:hover': {
                borderColor: '#1B998B',
                transform: 'scale(1.01)',
                boxShadow: '0 4px 20px rgba(27, 153, 139, 0.15)',
              },
            }}
            onDrop={handleFileDrop}
            onDragOver={(e) => e.preventDefault()}
            onClick={() => fileInputRef.current?.click()}
          >
            {!image ? (
              <Box sx={{ textAlign: 'center' }}>
                <CloudUploadIcon sx={{ fontSize: 80, color: '#2E1437', mb: 2 }} />
                <Typography 
                  variant="h5" 
                  gutterBottom 
                  fontWeight="bold" 
                  sx={{ color: '#2E1437', textShadow: '0 2px 4px rgba(0,0,0,0.1)' }}
                >
                  Drop your flower image here
                </Typography>
                <Typography variant="body1" sx={{ color: 'rgba(46, 20, 55, 0.7)' }}>
                  for crypto-botanical analysis
                </Typography>
              </Box>
            ) : (
              <Box sx={{ position: 'relative', width: '100%', height: '100%' }}>
                <img
                  src={image}
                  alt="Preview"
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'contain',
                  }}
                />
                <IconButton
                  sx={{
                    position: 'absolute',
                    top: 16,
                    right: 16,
                    backgroundColor: 'white',
                    boxShadow: 2,
                    '&:hover': {
                      backgroundColor: 'white',
                      transform: 'scale(1.1)',
                    },
                  }}
                  onClick={(e: React.MouseEvent) => {
                    e.stopPropagation();
                    clearImage();
                  }}
                >
                  <DeleteIcon color="error" />
                </IconButton>
              </Box>
            )}
          </Box>
        </Box>

        {/* Right Side - Controls */}
        <Box
          sx={{
            flex: '1',
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            gap: 3,
            justifyContent: 'center',
          }}
        >
          <input
            type="file"
            accept="image/*"
            hidden
            ref={fileInputRef}
            onChange={handleFileInput}
          />
          <Button
            fullWidth
            variant="contained"
            size="large"
            startIcon={<FileUploadIcon />}
            onClick={() => fileInputRef.current?.click()}
            sx={{
              py: 2,
              borderRadius: 2,
              textTransform: 'none',
              fontSize: '1.1rem',
              backgroundColor: '#1B998B',
              '&:hover': {
                backgroundColor: '#168577',
              },
            }}
          >
            Choose File
          </Button>
          <Button
            fullWidth
            variant="contained"
            size="large"
            disabled={!image}
            onClick={onSubmit}
            sx={{
              py: 2,
              borderRadius: 2,
              textTransform: 'none',
              fontSize: '1.1rem',
              backgroundColor: '#2E1437',
              '&:hover': {
                backgroundColor: '#231029',
              },
              '&.Mui-disabled': {
                backgroundColor: 'rgba(46, 20, 55, 0.3)',
              },
            }}
          >
            Submit Photo
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default ImageDrop;
