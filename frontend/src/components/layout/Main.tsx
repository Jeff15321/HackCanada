import React, { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import Home from './Home';
import Login from '../auth/Login';
import Signup from '../auth/Signup';
import { useUser } from '../../contexts/UserContext';
import Chat from './Chat'

interface MainProps {
    CurrentView: 'home' | 'chat';
}

const Main: React.FC<MainProps> = ({ CurrentView }) => {
    //user variables
    const { user, setUser } = useUser();

    //authentication variables
    const [isSignup, setIsSignup] = useState(false);

    useEffect(() => {
        if (localStorage.getItem('user')) {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            setUser(user);
        }
    }, []);


    if (!user) {
        return isSignup ? (
            <Signup/>
        ) : (
            <Login 
                onSignupClick={() => setIsSignup(true)}
            />
        );
    }
    
    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar isHome={CurrentView === 'home'} />
            
            <div className="flex-1">
                {CurrentView === 'home' ? (
                    <Home/>
                ) : (
                    <Chat />
                )}
            </div>
        </div>
    );
};

export default Main;