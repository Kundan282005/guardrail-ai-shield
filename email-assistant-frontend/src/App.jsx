import React, { useState } from 'react';

export default function App() {
  const [text, setText] = useState('');
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) {
      alert("Bhai pehle email content toh paste karo!");
      return;
    }
    setIsLoading(true);
    try {
      const response = await fetch('https://guardrail-ai-shield-1.onrender.com/api/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_text: text }),
      });
      const data = await response.json();
      setReport(data);
    } catch (error) {
      alert("Backend server (main.py) chalu hai na? Check karo!");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-gray-900 min-h-screen text-gray-100 font-sans antialiased">
      {/* Navbar */}
      <header className="bg-gray-800 border-b border-gray-700 py-4 shadow-lg">
        <div className="max-w-6xl mx-auto px-4 flex items-center justify-between">
          <h1 className="text-xl font-black tracking-wider text-cyan-400">
            
            GUARDRAIL <span className="text-gray-500 font-normal text-xs bg-gray-900 border border-gray-700 ml-2 px-2 py-0.5 rounded">V1.1</span>
          </h1>
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest">Enterprise Fraud Shield</p>
        </div>
      </header>

      {/* Main Grid */}
      <main className="max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Input Panel */}
        <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700 flex flex-col space-y-4">
          <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider">Inspect Incoming Email Payload</label>
          <textarea
            rows="12"
            className="w-full p-4 bg-gray-900 border border-gray-700 rounded-xl focus:ring-2 focus:ring-cyan-500 focus:outline-none transition text-sm text-gray-200 font-mono"
            placeholder="Paste raw email header or text body here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            onClick={handleAnalyze}
            disabled={isLoading}
            className={`w-full py-3 px-4 font-bold rounded-xl text-gray-900 transition flex items-center justify-center ${
              isLoading ? 'bg-cyan-600 opacity-50 cursor-not-allowed' : 'bg-cyan-400 hover:bg-cyan-300'
            }`}
          >
            {isLoading ? '⏳ Scanning Security Vectors...' : 'Analyze & Intercept'}
          </button>
        </div>

        {/* Dashboard/Output Panel */}
        <div className="space-y-6">
          {!report ? (
            <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700 flex items-center justify-center min-h-[400px] text-gray-500 text-sm font-mono border-dashed">
              [SYSTEM IDLE: Awaiting analysis trigger...]
            </div>
          ) : (
            <>
              {/* Security Shield Banner */}
              {report.fraud_analysis?.is_fraud ? (
                <div className="p-5 bg-red-950/50 border-2 border-red-500 text-red-200 rounded-2xl shadow-lg flex flex-col space-y-1">
                  <span className="font-black text-red-400 text-base tracking-wide">🚨 THREAT VECTOR IDENTIFIED</span>
                  <p className="text-sm">
                    Classified as <span className="font-bold text-red-300 underline">{report.fraud_analysis.category}</span> with <span className="font-black text-red-400">{report.fraud_analysis.confidence_score}%</span> ML match accuracy.
                  </p>
                </div>
              ) : (
                <div className="p-5 bg-emerald-950/40 border-2 border-emerald-500 text-emerald-200 rounded-2xl shadow-lg font-bold text-sm">
                  🛡️ VETTING COMPLETE: Payload verified as Secure/Non-Spam.
                </div>
              )}

              {/* Summary Box */}
              <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700">
                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3 border-b border-gray-700 pb-2">📋 AI Forensic Analysis</h3>
                <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-line font-mono">{report.summary}</div>
              </div>

              {/* Action Vector */}
              <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700">
                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3 border-b border-gray-700 pb-2">⚡ Protocol Mitigation Response</h3>
                {report.fraud_analysis?.is_fraud ? (
                  <div className="p-4 bg-red-900/30 text-red-300 rounded-xl border border-red-800/60 text-xs font-mono leading-relaxed">
                    ⚠️ CRITICAL PROTOCOL LOCK: Outbound transmission vector disabled. Automated drafts suspended to mitigate phishing link callback vectors.
                  </div>
                ) : (
                  <div className="p-4 bg-gray-900 text-gray-300 rounded-xl border border-gray-700 text-sm whitespace-pre-line font-mono">{report.reply}</div>
                )}
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}