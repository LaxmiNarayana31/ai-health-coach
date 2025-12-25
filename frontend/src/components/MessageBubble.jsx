import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { format } from 'date-fns';
import { CheckCheck } from 'lucide-react';

export default function MessageBubble({ message }) {
    const isUser = message.sender?.toLowerCase() === 'user';

    return (
        <div className={`flex w-full mb-2 ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div
                className={`max-w-[85%] px-4 py-2.5 rounded-2xl shadow-sm relative text-sm leading-relaxed ${isUser
                    ? 'bg-blue-600 text-white rounded-tr-sm'
                    : 'bg-white text-gray-800 border border-gray-100 rounded-tl-sm'
                    }`}
            >
                {/* Message Content */}
                <div className="leading-snug break-words markdown-content">
                    {isUser ? (
                        message.content
                    ) : (
                        <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                                p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                                ul: ({ node, ...props }) => <ul className="list-disc ml-4 mb-2" {...props} />,
                                ol: ({ node, ...props }) => <ol className="list-decimal ml-4 mb-2" {...props} />,
                                a: ({ node, ...props }) => <a className="text-blue-500 hover:underline" target="_blank" {...props} />,
                                code: ({ node, inline, className, children, ...props }) => {
                                    return inline ? (
                                        <code className="bg-gray-100 rounded px-1 py-0.5 text-xs font-mono" {...props}>{children}</code>
                                    ) : (
                                        <pre className="bg-gray-100 rounded p-2 overflow-x-auto text-xs font-mono mb-2" {...props}>
                                            <code>{children}</code>
                                        </pre>
                                    )
                                }
                            }}
                        >
                            {message.content}
                        </ReactMarkdown>
                    )}
                </div>

                {/* Metadata */}
                <div className={`flex items-center justify-end space-x-1 mt-1 select-none pointer-events-none ${isUser ? '-mr-1' : ''}`}>
                    <span className="text-[10px] text-gray-500 min-w-fit">
                        {message.created_at ? format(new Date(message.created_at), 'h:mm a') : ''}
                    </span>
                    {isUser && (
                        <span className="text-blue-500">
                            <CheckCheck size={14} />
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
}
