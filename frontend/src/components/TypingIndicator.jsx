import React from 'react';
import { motion } from 'framer-motion';

export default function TypingIndicator() {
    return (
        <div className="flex w-full mb-2 justify-start">
            <div className="bg-white px-4 py-3 rounded-lg rounded-tl-none shadow-[0_1px_0.5px_rgba(0,0,0,0.13)] flex items-center space-x-1">
                <span className="text-xs text-gray-400 mr-2">Disha is typing</span>
                {[0, 1, 2].map((dot) => (
                    <motion.div
                        key={dot}
                        className="w-1.5 h-1.5 bg-gray-400 rounded-full"
                        animate={{ y: [0, -4, 0] }}
                        transition={{ duration: 0.6, repeat: Infinity, delay: dot * 0.2 }}
                    />
                ))}
            </div>
        </div>
    );
}
