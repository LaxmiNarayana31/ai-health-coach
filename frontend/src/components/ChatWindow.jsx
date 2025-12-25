import React, { useState, useEffect, useRef } from 'react';
import client from '../api/client';
import { Send, ArrowUp, MoreVertical, Phone, Video, Smile, Plus, Mic } from 'lucide-react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';

export default function ChatWindow() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [userId, setUserId] = useState(localStorage.getItem('disha_user_id'));
    const [isLoadingHistory, setIsLoadingHistory] = useState(false);

    const scrollRef = useRef(null);
    const messagesEndRef = useRef(null);

    // Initialize Chat
    useEffect(() => {
        const initChat = async () => {
            if (!userId) {
                try {
                    // New User Onboarding
                    const res = await client.post('/chat/init', { user_id: null });
                    setUserId(res.data.data.user_id);
                    localStorage.setItem('disha_user_id', res.data.data.user_id);
                    setMessages([{
                        id: Date.now(),
                        sender: 'Disha',
                        content: res.data.data.message.content,
                        created_at: new Date().toISOString()
                    }]);
                } catch (err) {
                    console.error("Init failed", err);
                }
            } else {
                // Load initial history
                loadHistory();
            }
        };
        initChat();
    }, []);

    // Auto-scroll to bottom on new message if near bottom or first load
    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const loadHistory = async (beforeId = null) => {
        if (!userId) return;
        setIsLoadingHistory(true);
        try {
            const params = { user_id: userId, limit: 20 };
            if (beforeId) params.before_id = beforeId;

            const res = await client.get('/chat/history', { params });
            const newMessages = res.data.data.messages;

            if (newMessages.length > 0) {
                if (beforeId) {
                    // Prepend
                    setMessages(prev => [...newMessages, ...prev]);
                } else {
                    // Initial load
                    setMessages(newMessages);
                }
            }
        } catch (err) {
            console.error("Failed to load history", err);
        } finally {
            setIsLoadingHistory(false);
        }
    };

    const handleScroll = (e) => {
        if (e.target.scrollTop === 0 && messages.length > 0 && !isLoadingHistory) {
            const oldestId = messages[0].id;
            // Prevent fetching if oldestId is temporary (timestamp based)
            if (typeof oldestId === 'number') {
                loadHistory(oldestId);
            }
        }
    };

    const sendMessage = async (e) => {
        if (e && e.preventDefault) e.preventDefault();
        if (!input.trim() || !userId) return;

        const userMsg = {
            id: Date.now(), // Temp ID
            sender: 'User',
            content: input,
            created_at: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsTyping(true);

        try {
            const res = await client.post('/chat/message', {
                user_id: userId,
                message: userMsg.content
            });

            const aiMsg = {
                id: res.data.data.id,
                sender: 'Disha',
                content: res.data.data.content,
                created_at: res.data.data.created_at || new Date().toISOString()
            };

            setMessages(prev => [...prev, aiMsg]);
        } catch (err) {
            console.error("Send failed", err);
            // Ideally show error state
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-slate-50 w-full shadow-xl overflow-hidden sm:border-x border-gray-200 relative">
            {/* Header */}
            <div className="bg-white p-4 shadow-sm z-10 flex items-center justify-between border-b border-gray-100">
                <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold shadow-sm">
                        D
                    </div>
                    <div>
                        <h1 className="font-semibold text-base text-gray-800 leading-tight">Disha Health Coach</h1>
                        <p className="text-[11px] text-green-600 font-medium leading-tight flex items-center gap-1">
                            <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                            Online
                        </p>
                    </div>
                </div>
            </div>

            {/* Chat Area */}
            <div
                className="flex-1 overflow-y-auto p-4 space-y-3 pb-4"
                onScroll={handleScroll}
                ref={scrollRef}
            >
                {isLoadingHistory && (
                    <div className="flex justify-center py-4">
                        <div className="bg-gray-100 rounded-full px-3 py-1">
                            <span className="text-xs text-gray-500 flex items-center gap-2">
                                <span className="w-3 h-3 border-2 border-gray-400 border-t-blue-600 rounded-full animate-spin"></span>
                                Loading history...
                            </span>
                        </div>
                    </div>
                )}

                {messages.map((msg, index) => (
                    <MessageBubble key={index} message={msg} />
                ))}

                {isTyping && <TypingIndicator />}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="bg-white p-4 border-t border-gray-100 z-10">
                <div className="flex items-center space-x-2 bg-gray-50 rounded-xl px-2 py-2 border border-gray-200 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-100 transition-all shadow-sm">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && sendMessage(e)}
                        placeholder="Type your health query..."
                        className="flex-1 bg-transparent border-none focus:ring-0 text-base py-2 px-3 outline-none text-gray-700 placeholder:text-gray-400"
                    />
                    <button
                        onClick={sendMessage}
                        disabled={!input.trim() || isTyping}
                        className={`p-2.5 rounded-lg transition-all duration-200 flex items-center justify-center ${input.trim() ? 'bg-blue-600 text-white shadow-md hover:bg-blue-700 active:scale-95' : 'bg-gray-200 text-gray-400 cursor-not-allowed'}`}
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
}
