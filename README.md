# Echo Mind 🧠

### Autonomous AI Content Intelligence Platform

Echo Mind is an autonomous AI-powered content intelligence system that discovers relevant technology news, evaluates its importance, uses contextual memory to avoid repetitive decisions, and automatically publishes valuable content.

The system is designed to operate as an intelligent editorial pipeline rather than a simple news aggregator.

---

## 🚀 How Echo Mind Works

```text
Real-Time News Sources
        ↓
Discovery Engine
        ↓
Topic Scoring
        ↓
AI Editorial Evaluation
        ↓
Contextual Memory
        ↓
Duplicate Detection
        ↓
Publishing Engine
        ↓
Content Feed
```

Echo Mind continuously transforms raw technology news into evaluated and publishable content through an automated workflow.

---

## ✨ Key Features

* 📰 **Real-Time News Discovery** using RSS feeds
* 🎯 **Intelligent Topic Scoring** based on relevance and importance
* 🤖 **Autonomous Editorial Decisions**
* 🧠 **Contextual Long-Term Memory** powered by Breeth
* ♻️ **Duplicate Prevention** across agent runs
* 🚀 **Automated Content Publishing**
* 👤 **Agent-Specific Memory**
* ⚡ **REST API** for frontend integration
* 📡 **Live Content Feed**
* 🧩 **Modular & Scalable Architecture**

---

## 🏗️ Architecture

Echo Mind follows a modular backend architecture:

```text
                    ┌──────────────────┐
                    │   News Sources   │
                    │   RSS / Google   │
                    │       News       │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Discovery Engine │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │  Topic Scoring   │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Editorial Engine │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │  Memory Engine   │
                    │ Breeth + SQLite  │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Publishing Engine│
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │   Content Feed   │
                    └──────────────────┘
```

---

## 🧠 Intelligent Memory

Echo Mind uses **Breeth** as a contextual memory layer.

The memory system allows the platform to:

* Retrieve related historical context
* Remember previous editorial decisions
* Maintain agent-specific topic history
* Prevent repeated publishing
* Improve contextual decision-making over time

SQLite is used for structured local memory and publishing records.

---

## 🔌 API

The backend exposes REST APIs for frontend and external integration.

### Run Agent

```http
POST /api/agent/run?agentId={agent_id}
```

Triggers the complete autonomous workflow.

### Health Check

```http
GET /api/health
```

Checks whether the backend is running.

### Content Feed

```http
GET /api/feed
```

Returns published content for the frontend.

Interactive API documentation is available through FastAPI's Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## 🛠️ Technology Stack

| Layer                | Technology          |
| -------------------- | ------------------- |
| Backend              | Python              |
| API Framework        | FastAPI             |
| Server               | Uvicorn             |
| News Discovery       | RSS / Google News   |
| AI & Editorial Logic | AI-powered services |
| Contextual Memory    | Breeth              |
| Structured Storage   | SQLite              |
| API Documentation    | Swagger / OpenAPI   |

---

## 📁 Project Structure

```text
Echo/
│
├── Backend/
│   ├── agents/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── memory/
│   ├── scheduler/
│   ├── schemas/
│   ├── services/
│   ├── tests/
│   ├── utils/
│   ├── main.py
│   ├── worker.py
│   └── requirements.txt
│
├── Frontend/
│
└── docs/
    └── README.md
```

---

## 🧪 Tested Workflow

The backend has been tested with real RSS feeds and successfully demonstrated:

```text
Discover
   ↓
Score
   ↓
Evaluate
   ↓
Check Memory
   ↓
Publish / Skip
```

The system has successfully:

* Discovered multiple real technology articles
* Scored and ranked topics
* Detected previously processed topics
* Skipped duplicate content
* Stored decisions in memory
* Published approved content
* Returned results through the REST API

---

## 🎯 Vision

Echo Mind aims to move beyond traditional content aggregation by creating an **autonomous editorial intelligence layer** that can discover, understand, remember, evaluate, and publish content with minimal human intervention.

> **Discover. Understand. Remember. Decide. Publish.**

---

## 👥 Team

Built with ❤️ by the Echo Mind team.
