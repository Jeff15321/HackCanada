import "../styles/globals.css";

import type { AppProps } from "next/app";
import { UserProvider } from "../contexts/UserContext";
import { ModelProvider } from "../contexts/ModalContext";

export default function App({ Component, pageProps }: AppProps) {
  return (
      <UserProvider>  
        <ModelProvider>
          <Component {...pageProps} /> 
        </ModelProvider>
      </UserProvider>
  );
}

