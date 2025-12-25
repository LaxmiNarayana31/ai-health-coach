import React from 'react';
import ChatWindow from './components/ChatWindow';

function App() {
  return (
    <div className="h-screen bg-[#d1d7db] flex items-center justify-center sm:p-4">
      <div className="w-full h-full sm:h-[90vh] sm:max-w-md block">
        <ChatWindow />
      </div>
    </div>
  );
}

export default App;
