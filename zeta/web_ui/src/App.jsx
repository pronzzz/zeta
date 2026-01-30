import { useState, useEffect, useRef } from 'react'

function App() {
  const [messages, setMessages] = useState([
    { role: 'agent', content: 'Hello! I am Zeta. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [stats, setStats] = useState({ cpu_cores: 0, ram_total: 0, memory_count: 0, model: 'Loading...' });
  const [activeTab, setActiveTab] = useState('dashboard'); // dashboard | chat | memories
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages, activeTab]);

  // Fetch Stats Loop
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('http://localhost:8000/stats');
        const data = await res.json();
        setStats(data);
      } catch (e) {
        console.error("Stats fetch failed", e);
      }
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.content }),
      });

      const data = await response.json();
      const agentMsg = { role: 'agent', content: data.response };
      setMessages(prev => [...prev, agentMsg]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'agent', content: 'Error connecting to Zeta backend.' }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex h-screen bg-slate-100 font-sans text-slate-900 overflow-hidden">

      {/* Sidebar - One UI Style (Curved right edge?) */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between py-6 px-4 z-20 shadow-sm hidden md:flex">
        <div>
          <div className="mb-10 px-2">
            <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">Zeta Agent</h1>
            <p className="text-xs text-slate-400 font-medium mt-1">v1.0 • One UI 8 Inspired</p>
          </div>

          <nav className="space-y-1">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-2xl transition-all duration-200 ${activeTab === 'dashboard' ? 'bg-blue-50 text-blue-700 font-semibold shadow-sm' : 'text-slate-500 hover:bg-slate-50'}`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
              <span>Dashboard</span>
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-2xl transition-all duration-200 ${activeTab === 'chat' ? 'bg-blue-50 text-blue-700 font-semibold shadow-sm' : 'text-slate-500 hover:bg-slate-50'}`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
              <span>Chat</span>
            </button>
            <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-2xl text-slate-500 hover:bg-slate-50 transition-all cursor-not-allowed opacity-50">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
              <span>Memory (Soon)</span>
            </button>
          </nav>
        </div>

        <div className="px-4 py-4 bg-slate-50 rounded-3xl mx-2 mb-2">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">System</h3>
          <div className="flex justify-between text-xs text-slate-600 mb-1">
            <span>CPU Cores</span>
            <span className="font-bold">{stats.cpu_cores}</span>
          </div>
          <div className="flex justify-between text-xs text-slate-600">
            <span>RAM</span>
            <span className="font-bold">{stats.ram_total} GB</span>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col relative overflow-hidden">

        {/* Header (Top Bar) */}
        <header className="h-16 bg-white/50 backdrop-blur-md border-b border-white/50 flex items-center justify-between px-8 sticky top-0 z-10">
          <h2 className="text-xl font-bold text-slate-800">{activeTab === 'dashboard' ? 'System Overview' : 'Agent Chat'}</h2>
          <div className="flex items-center space-x-2 bg-white px-3 py-1.5 rounded-full shadow-sm border border-slate-100">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs font-medium text-slate-600">Model: {stats.model}</span>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-4 sm:p-8 space-y-8 scrollbar-hide">

          {activeTab === 'dashboard' && (
            <div className="animate-fade-in space-y-6 max-w-5xl mx-auto">
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                  <div className="flex items-center space-x-4">
                    <div className="p-3 bg-blue-50 text-blue-600 rounded-2xl">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                    </div>
                    <div>
                      <p className="text-sm text-slate-500 font-medium">Memory Items</p>
                      <p className="text-2xl font-bold text-slate-800">{stats.memory_count}</p>
                    </div>
                  </div>
                </div>
                <div className="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                  <div className="flex items-center space-x-4">
                    <div className="p-3 bg-purple-50 text-purple-600 rounded-2xl">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                    </div>
                    <div>
                      <p className="text-sm text-slate-500 font-medium">Status</p>
                      <p className="text-2xl font-bold text-green-600">Online</p>
                    </div>
                  </div>
                </div>
                <div className="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                  <div className="flex items-center space-x-4">
                    <div className="p-3 bg-orange-50 text-orange-600 rounded-2xl">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                    </div>
                    <div>
                      <p className="text-sm text-slate-500 font-medium">Session ID</p>
                      <p className="text-sm font-mono text-slate-600 truncate max-w-[120px]">Local</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Quick Access to Chat */}
              <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-[2.5rem] p-8 text-white shadow-xl relative overflow-hidden group cursor-pointer" onClick={() => setActiveTab('chat')}>
                <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -translate-y-1/2 translate-x-1/4 group-hover:scale-110 transition-transform duration-500"></div>
                <h3 className="text-3xl font-bold mb-2 relative z-10">Start a Conversation</h3>
                <p className="text-blue-100 max-w-md relative z-10 mb-6">Ask Zeta to search the web, check stocks, or manage your system.</p>
                <button className="px-6 py-3 bg-white text-blue-700 font-bold rounded-xl shadow-lg hover:shadow-xl hover:bg-blue-50 transition-all flex items-center space-x-2">
                  <span>Open Chat</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                </button>
              </div>
            </div>
          )}

          {/* Chat View */}
          {activeTab === 'chat' && (
            <div className="flex-1 flex flex-col h-full max-w-4xl mx-auto w-full">
              <div className="flex-1 overflow-y-auto space-y-6 pb-24">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
                  >
                    <div
                      className={`max-w-[85%] p-5 text-[15px] leading-relaxed shadow-sm
                                ${msg.role === 'user'
                          ? 'bg-blue-600 text-white rounded-[1.5rem] rounded-tr-sm'
                          : 'bg-white text-slate-800 rounded-[1.5rem] rounded-tl-sm border border-slate-100'
                        }`}
                    >
                      <div dangerouslySetInnerHTML={{ __html: msg.content.replace(/\n/g, '<br/>') }} />
                    </div>
                  </div>
                ))}
                {isTyping && (
                  <div className="flex justify-start animate-fade-in">
                    <div className="bg-white px-5 py-4 rounded-[1.5rem] rounded-tl-sm shadow-sm border border-slate-100 flex items-center space-x-1.5">
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-0"></div>
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Floating Input */}
              <div className="absolute bottom-6 left-0 right-0 px-4 sm:px-8 max-w-4xl mx-auto w-full">
                <div className="flex items-center bg-white/90 backdrop-blur-xl rounded-full shadow-2xl border border-slate-200/50 p-2">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Ask Zeta anything..."
                    className="flex-1 bg-transparent border-none focus:ring-0 px-6 py-3 text-slate-700 placeholder-slate-400 outline-none"
                    autoFocus
                  />
                  <button
                    onClick={sendMessage}
                    disabled={!input.trim() || isTyping}
                    className={`p-4 rounded-full transition-all duration-300 transform
                              ${input.trim()
                        ? 'bg-blue-600 text-white hover:bg-blue-700 hover:rotate-90 shadow-lg'
                        : 'bg-slate-100 text-slate-300 cursor-not-allowed'}`}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                      <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
