import "../styles/globals.css";

import type { AppProps } from "next/app";
import { UserProvider } from "../contexts/UserContext";
import { ProjectProvider } from "../contexts/ProjectContext";
import { ChatHistoryProvider } from "../contexts/chat/ChatHistoryContext";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ChatHistoryProvider>

        <UserProvider>  
          <ProjectProvider>
            <Component {...pageProps} /> 
          </ProjectProvider>
        </UserProvider>
    </ChatHistoryProvider>
  );
}

