import { useLocation } from "wouter";

export default function Home() {
  const [, navigate] = useLocation();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl mx-auto text-center">
        <h1 className="text-5xl font-bold text-white mb-4">Video Chat Editor</h1>
        <p className="text-xl text-slate-300 mb-8">
          AI-powered video editing with natural language commands
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="bg-slate-700 p-6 rounded-lg border border-slate-600 hover:border-slate-500 transition">
            <div className="text-3xl mb-3">🎬</div>
            <h3 className="text-lg font-semibold text-white mb-2">Edit Videos</h3>
            <p className="text-slate-400">
              Trim, cut, and merge video segments with AI precision
            </p>
          </div>
          
          <div className="bg-slate-700 p-6 rounded-lg border border-slate-600 hover:border-slate-500 transition">
            <div className="text-3xl mb-3">💬</div>
            <h3 className="text-lg font-semibold text-white mb-2">Chat Commands</h3>
            <p className="text-slate-400">
              Simply type what you want: "remove silence" or "cut from 1:20 to 2:10"
            </p>
          </div>
          
          <div className="bg-slate-700 p-6 rounded-lg border border-slate-600 hover:border-slate-500 transition">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="text-lg font-semibold text-white mb-2">Instant Results</h3>
            <p className="text-slate-400">
              Get processed videos in seconds with powerful AI processing
            </p>
          </div>
        </div>

        <div className="mt-12">
          <button 
            onClick={() => navigate("/editor")}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition transform hover:scale-105"
          >
            Get Started →
          </button>
        </div>

        <p className="text-slate-500 mt-8 text-sm">
          Upload a video and use chat commands to edit
        </p>
      </div>
    </div>
  );
}
