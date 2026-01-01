'use client';

import { useState, useRef, useEffect } from 'react';
import { useLocation } from 'wouter';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Loader2, Upload, Send, Download, X } from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  operation?: string;
  outputPath?: string;
  status?: string;
}

export default function Editor() {
  const [, navigate] = useLocation();
  const [videoId, setVideoId] = useState<string>('');
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [videoPreview, setVideoPreview] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_BASE = 'http://127.0.0.1:8000/api';

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('video/')) {
      addMessage('assistant', '❌ Please select a valid video file (MP4, AVI, MOV, etc.)');
      return;
    }

    setVideoFile(file);
    const preview = URL.createObjectURL(file);
    setVideoPreview(preview);
    addMessage('assistant', `✓ Video selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)}MB)`);
  };

  const uploadVideo = async () => {
    if (!videoFile) {
      addMessage('assistant', '❌ Please select a video file first');
      return;
    }

    setUploading(true);
    addMessage('assistant', '⏳ Uploading video...');

    try {
      const formData = new FormData();
      formData.append('file', videoFile);

      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      const data = await response.json();
      setVideoId(data.video_id);
      addMessage('assistant', `✓ Video uploaded successfully!\n\nID: ${data.video_id}\n\nYou can now use chat commands to edit. Try:\n• "remove silence"\n• "cut from 00:01:20 to 00:02:10"\n• "trim to 60 seconds"\n• "transcribe"\n• "resize to 1280x720"`);
    } catch (error) {
      addMessage('assistant', `❌ Upload failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setUploading(false);
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    if (!videoId) {
      addMessage('assistant', '❌ Please upload a video first');
      return;
    }

    addMessage('user', inputValue);
    setInputValue('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          video_id: videoId,
          message: inputValue,
        }),
      });

      const data = await response.json();

      if (data.status === 'success' || data.status === 'processing') {
        addMessage(
          'assistant',
          `✓ ${data.message}\n\n${data.operation ? `Operation: ${data.operation}` : ''}${data.outputPath ? `\n\nOutput: ${data.outputPath}` : ''}`,
          data.operation,
          data.outputPath,
          data.status
        );

        // Check status periodically
        if (data.status === 'processing') {
          checkStatus(videoId);
        }
      } else {
        addMessage('assistant', `❌ ${data.message}`);
      }
    } catch (error) {
      addMessage('assistant', `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const checkStatus = async (id: string) => {
    try {
      const response = await fetch(`${API_BASE}/status/${id}`);
      const data = await response.json();

      if (data.status === 'complete') {
        addMessage('assistant', `✓ Processing complete! Your video is ready to download.`);
      }
    } catch (error) {
      console.error('Status check failed:', error);
    }
  };

  const downloadVideo = async () => {
    if (!videoId) return;

    try {
      const response = await fetch(`${API_BASE}/download/${videoId}`);
      if (!response.ok) throw new Error('Download failed');

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `edited_video_${videoId.slice(0, 8)}.mp4`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      addMessage('assistant', '✓ Video downloaded!');
    } catch (error) {
      addMessage('assistant', `❌ Download failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const addMessage = (
    type: 'user' | 'assistant',
    content: string,
    operation?: string,
    outputPath?: string,
    status?: string
  ) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      type,
      content,
      timestamp: new Date(),
      operation,
      outputPath,
      status,
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const clearChat = () => {
    setMessages([]);
    setVideoId('');
    setVideoFile(null);
    setVideoPreview('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Header */}
      <div className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white cursor-pointer hover:text-blue-400" onClick={() => navigate('/')}>
              Video Chat Editor
            </h1>
            <p className="text-slate-400 text-sm">AI-powered video editing with natural language</p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="text-slate-400 hover:text-white transition"
          >
            ← Back
          </button>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left: Video Upload & Preview */}
          <div className="space-y-6">
            <Card className="p-6 bg-slate-800 border-slate-700">
              <h2 className="text-xl font-semibold text-white mb-4">📹 Upload Video</h2>

              {videoPreview ? (
                <div className="space-y-4">
                  <video
                    src={videoPreview}
                    className="w-full rounded-lg bg-black"
                    controls
                    style={{ maxHeight: '300px' }}
                  />
                  <button
                    onClick={() => {
                      setVideoPreview('');
                      setVideoFile(null);
                      if (fileInputRef.current) fileInputRef.current.value = '';
                    }}
                    className="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded flex items-center justify-center gap-2 transition"
                  >
                    <X size={16} /> Clear
                  </button>
                </div>
              ) : (
                <div
                  onClick={() => fileInputRef.current?.click()}
                  className="border-2 border-dashed border-slate-600 rounded-lg p-8 text-center cursor-pointer hover:border-slate-500 transition"
                >
                  <Upload className="mx-auto mb-2 text-slate-400" size={32} />
                  <p className="text-slate-300 font-medium">Click to select video</p>
                  <p className="text-slate-500 text-sm">MP4, AVI, MOV, MKV (max 500MB)</p>
                </div>
              )}

              <input
                ref={fileInputRef}
                type="file"
                accept="video/*"
                onChange={handleFileSelect}
                className="hidden"
              />

              {videoFile && !videoId && (
                <button
                  onClick={uploadVideo}
                  disabled={uploading}
                  className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded font-medium transition disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {uploading ? (
                    <>
                      <Loader2 size={16} className="animate-spin" /> Uploading...
                    </>
                  ) : (
                    <>
                      <Upload size={16} /> Upload Video
                    </>
                  )}
                </button>
              )}

              {videoId && (
                <div className="mt-4 p-3 bg-green-900/30 border border-green-700 rounded text-green-300 text-sm">
                  ✓ Video ready for editing
                </div>
              )}
            </Card>

            {/* Quick Commands */}
            <Card className="p-6 bg-slate-800 border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">💡 Quick Commands</h3>
              <div className="space-y-2 text-sm">
                <button
                  onClick={() => setInputValue('remove silence')}
                  className="w-full text-left p-2 hover:bg-slate-700 rounded text-slate-300 hover:text-white transition"
                >
                  Remove silence
                </button>
                <button
                  onClick={() => setInputValue('cut from 00:00:10 to 00:00:30')}
                  className="w-full text-left p-2 hover:bg-slate-700 rounded text-slate-300 hover:text-white transition"
                >
                  Cut segment
                </button>
                <button
                  onClick={() => setInputValue('trim to 60 seconds')}
                  className="w-full text-left p-2 hover:bg-slate-700 rounded text-slate-300 hover:text-white transition"
                >
                  Trim duration
                </button>
                <button
                  onClick={() => setInputValue('transcribe')}
                  className="w-full text-left p-2 hover:bg-slate-700 rounded text-slate-300 hover:text-white transition"
                >
                  Get transcript
                </button>
                <button
                  onClick={() => setInputValue('speed up 1.5x')}
                  className="w-full text-left p-2 hover:bg-slate-700 rounded text-slate-300 hover:text-white transition"
                >
                  Change speed
                </button>
              </div>
            </Card>

            {videoId && (
              <button
                onClick={downloadVideo}
                className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded font-medium transition flex items-center justify-center gap-2"
              >
                <Download size={16} /> Download Latest
              </button>
            )}
          </div>

          {/* Right: Chat Interface */}
          <div className="lg:col-span-2">
            <Card className="h-full bg-slate-800 border-slate-700 flex flex-col">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4" style={{ maxHeight: '600px' }}>
                {messages.length === 0 && (
                  <div className="text-center text-slate-400 py-12">
                    <p className="text-lg font-medium mb-2">👋 Welcome to Video Chat Editor</p>
                    <p className="text-sm">Upload a video to get started, then use natural language commands to edit it.</p>
                  </div>
                )}

                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs px-4 py-2 rounded-lg whitespace-pre-wrap text-sm ${
                        msg.type === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-slate-700 text-slate-100'
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}

                <div ref={messagesEndRef} />
              </div>

              {/* Input */}
              <div className="border-t border-slate-700 p-4">
                <form onSubmit={sendMessage} className="flex gap-2">
                  <Input
                    type="text"
                    placeholder={videoId ? "Describe what to do with your video..." : "Upload a video first..."}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    disabled={!videoId || loading}
                    className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
                  />
                  <Button
                    type="submit"
                    disabled={!videoId || loading || !inputValue.trim()}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    {loading ? (
                      <Loader2 size={16} className="animate-spin" />
                    ) : (
                      <Send size={16} />
                    )}
                  </Button>
                </form>
              </div>

              {messages.length > 0 && (
                <div className="border-t border-slate-700 px-4 py-2 flex justify-center">
                  <button
                    onClick={clearChat}
                    className="text-xs text-slate-400 hover:text-slate-300 transition"
                  >
                    Clear conversation
                  </button>
                </div>
              )}
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
