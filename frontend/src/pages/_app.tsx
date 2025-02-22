import "../styles/globals.css";

import type { AppProps } from "next/app";
import { UserProvider } from "../contexts/UserContext";
import { ModelProvider } from "../contexts/Model";
import { ImageProvider } from '../contexts/ImageContext';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ImageProvider>
      <UserProvider>  
        <ModelProvider>
          <Component {...pageProps} /> 
        </ModelProvider>
      </UserProvider>
    </ImageProvider>
  );
}

