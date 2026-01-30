# Zeta: Local Autonomous AI Agent 🧠

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-purple)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20Web-orange)

**Zeta** is a privacy-first, autonomous AI agent that runs 100% locally on your machine. It combines a secure terminal interface with a modern, "One UI 8" inspired Web Dashboard.

Unlike cloud agents, Zeta stores all memories, logs, and data on your device. It connects to **Ollama** for intelligence (Llama 3, DeepSeek, etc.) and uses **ChromaDB** for long-term semantic memory.

---

## ✨ Key Features

### 🧠 Intelligent Core
-   **Natural Language Understanding**: Speak naturally (e.g., *"Search for SpaceX news"* or *"Check NVDA stock"*).
-   **Long-Term Memory**: Remembers facts about you and past conversations across sessions using Vector Search (ChromaDB) and SQL.
-   **Local Inference**: Powered by Ollama. Zero data leaves your machine unless you ask for a Web Search.

### 💻 Dual Interface
1.  **Secure Terminal CLI**: Fast, keyboard-centric interface for developers.
2.  **Modern Web Dashboard**:
    -   **System Stats**: Real-time CPU/RAM monitoring.
    -   **Memory Visualization**: See how many facts Zeta has stored.
    -   **Chat Interface**: Beautiful, fluid chat experience.

### 🛠️ Powerful Skills
-   **Web Search**: Uses DuckDuckGo to find real-time info.
-   **Finance**: Live stock market data.
-   **System Control**: Can execute terminal commands (with safety confirmations).
-   **Note Taking**: Saves thoughts and ideas to local files.

---

## 🚀 Quick Start

### Prerequisites
-   **Python 3.10+**
-   **Node.js & npm** (for Web Dashboard)
-   **Ollama** (Running locally with a model like `llama3` or `deepseek-r1`)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/pronzzz/zeta.git
    cd zeta
    ```

2.  **Run the Installer**
    This script sets up the Python virtual environment and installs dependencies.
    ```bash
    ./install_zeta.sh
    ```

3.  **Start Zeta**
    To launch both the Backend Agent and the Web Dashboard:
    ```bash
    zeta start
    ```
    *Access the Dashboard at `http://localhost:5173`*

---

## 📖 Usage Guide

### Voice / Text Commands
Zeta's Intent Router understands context. Try these:

-   **Research**: *"Find the latest news on Artificial General Intelligence."*
-   **Finance**: *"What is the price of Apple stock?"*
-   **Memory**: *"My name is Pranav and I like coding."* -> *Later: "What is my name?"*
-   **System**: *"List files in this directory."* (Prompts for approval).

### Configuration
Edit `config.yaml` to customize:
-   **LLM Model**: Change `llm.model` to any model available in Ollama.
-   **Risk Tolerance**: Set `safety.risk_tolerance` to `high` to reduce confirmation prompts.

---

## 🏗️ Architecture

```mermaid
graph TD
    User[User] -->|Input| Router[Intent Router]
    Router -->|Chat| LLM[Ollama LLM]
    Router -->|Search| Web[Web Search Skill]
    Router -->|System| Sys[System Skill]
    
    LLM --> Memory[Memory Manager]
    Memory --> SQL[SQLite (Session History)]
    Memory --> Vector[ChromaDB (Long-term Facts)]
    
    API[FastAPI Server] -->|Exposes| Agent
    Dashboard[React Web UI] -->|Connects| API
```

---

## 🤝 Contributing
Contributions are welcome! Please read `CONTRIBUTING.md` (coming soon) for details.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built with ❤️ by Pranav Dwivedi*
