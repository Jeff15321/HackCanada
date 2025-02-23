import React from 'react';
import WalletLogin from '../auth/WalletLogin';

const Profile = () => {
  return (
    <WalletLogin>
      <div className="min-h-screen w-full bg-black p-8">
        <div className="bg-gray-900 rounded-xl p-8 border border-cyan-400/20">
          <h1 className="text-2xl font-bold text-white mb-4">User Profile</h1>
          <p className="text-gray-400">Profile content coming soon...</p>
        </div>
      </div>
    </WalletLogin>
  );
};

export default Profile; 