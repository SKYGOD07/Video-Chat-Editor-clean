'use client';

import { useLocation } from "wouter";
import { Button } from "@/components/ui/button";

export default function Home() {
  const [, navigate] = useLocation();

  const handleGetStarted = () => {
    console.log("Get Started button clicked");
    navigate("/editor");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl mx-auto text-center">
        <h1 className="text-5xl font-bold text-white mb-4">Video Chat Editor</h1>
        <p className="text-xl text-slate-300 mb-8">
          A powerful tool for editing and managing video chats with real-time collaboration
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="bg-slate-700 p-6 rounded-lg border border-slate-600 hover:border-slate-500 transition">
            <div className="text-3xl mb-3">✂️</div>
            <h3 className="text-lg font-semibold text-white mb-2">Edit Videos</h3>
            <p className="text-slate-400">
              Trim, cut, and merge video segments with precision
            </p>
          </div>
          
          <div className="bg-slate-700 p-6 rounded-lg border border-slate-600 hover:border-slate-500 transition">
            <div className="text-3xl mb-3">🎙️</div>
            <h3 className="text-lg font-semibold text-white mb-2">Audio Control</h3>
            <p className="text-slate-400">
              Adjust audio levels and manage multiple tracks
            </p>
          </div>
          
          <div className="bg-slate-700 p-6 rounded-lg border border-slate-600 hover:border-slate-500 transition">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="text-lg font-semibold text-white mb-2">Real-time Sync</h3>
            <p className="text-slate-400">
              Collaborate and sync changes instantly
            </p>
          </div>
        </div>

        <div className="mt-12">
          <Button 
            onClick={handleGetStarted}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-6 px-8 rounded-lg transition transform hover:scale-105 text-lg"
          >
            Get Started →
          </Button>
        </div>

        <p className="text-slate-500 mt-8 text-sm">
          Upload a video and use commands to edit
        </p>
      </div>
    </div>
  );
}
