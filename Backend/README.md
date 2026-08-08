# Echo Mind — Backend

## Overview

Echo Mind is an autonomous AI content intelligence system that discovers technology news, evaluates its importance, checks contextual memory, and automatically publishes relevant content.

The backend is built with **Python, FastAPI, SQLite, RSS feeds, and Breeth memory**.

---

## Core Workflow

```text
RSS News Sources
       ↓
Discovery Engine
       ↓
Topic Normalization & Scoring
       ↓
Breeth Context
       ↓
Editorial Engine
       ↓
Memory Check
       ↓
Publishing Engine
       ↓
Database
```

---

## Backend Components

### Discovery Engine

Responsible for discovering and preparing technology topics.

* Fetches real-time AI and technology news through RSS feeds.
* Normalizes article data.
* Removes duplicate topics.
* Calculates importance scores.
* Ranks topics based on relevance.

### Editorial Engine

Responsible for evaluating discovered topics.

* Analyzes topic relevance.
* Determines whether a topic should be published.
* Generates an editorial decision.
* Assigns an importance/editorial score.

### Memory Engine

Responsible for maintaining topic history and contextual memory.

* Maintains agent-specific memory in SQLite.
* Prevents duplicate publishing.
* Retrieves related context from Breeth.
* Stores editorial decisions and topic history.

### Publishing Engine

Responsible for publishing approved topics.

* Publishes approved content.
* Stores published posts in the database.
* Associates published content with the executing agent.

### Breeth Integration

Breeth acts as the contextual memory layer for Echo Mind.

It is used to:

* Retrieve related knowledge.
* Store editorial decisions.
* Maintain long-term context.
* Support contextual decision-making.

---

## API Endpoints

### Run Agent

```http
POST /api/agent/run?agentId={agent_id}
```

Runs the complete autonomous Echo Mind workflow.

### Health Check

```http
GET /api/health
```

Checks backend availability.

### Content Feed

```http
GET /api/feed
```

Returns published content for the frontend.

### API Documentation

When the backend is running, interactive Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Technology Stack

* **Language:** Python
* **Framework:** FastAPI
* **Server:** Uvicorn
* **News Discovery:** RSS / Google News
* **Memory:** Breeth + SQLite
* **Database:** SQLite
* **API Documentation:** Swagger / OpenAPI

---

## Key Features

* Real-time AI and technology news discovery
* Topic normalization and ranking
* AI-focused importance scoring
* Autonomous editorial decisions
* Contextual long-term memory
* Agent-specific memory
* Duplicate topic prevention
* Automated publishing
* REST API integration
* Modular backend architecture

---

## Backend Structure

```text
Backend/
│
├── agents/
│   ├── discovery_engine.py
│   ├── editorial_engine.py
│   ├── memory_engine.py
│   ├── orchestrator.py
│   ├── persona_engine.py
│   └── publishing_engine.py
│
├── api/
│   ├── feed.py
│   ├── health.py
│   ├── init.py
│   └── run.py
│
├── core/
│   ├── config.py
│   ├── constants.py
│   └── prompts.py
│
├── database/
│   ├── crud.py
│   ├── database.py
│   └── models.py
│
├── memory/
│   └── memory_store.py
│
├── scheduler/
│   ├── __init__.py
│   └── scheduler.py
│
├── schemas/
│   ├── __init__.py
│   └── agent.py
│
├── services/
│   ├── ai_service.py
│   ├── breeth_service.py
│   ├── news_service.py
│   ├── post_service.py
│   └── source_validator.py
│
├── tests/
│   ├── __init__.py
│   └── test_breeth.py
│
├── utils/
│   ├── helpers.py
│   ├── logger.py
│   └── scoring.py
│
├── main.py
├── worker.py
└── requirements.txt
```

---

## End-to-End Validation

The backend has been tested with real RSS news sources.

The autonomous workflow successfully performs:

```text
Discover
   ↓
Normalize
   ↓
Score
   ↓
Evaluate
   ↓
Check Memory
   ↓
Publish / Skip
```

The system successfully discovered **40 real technology topics** during testing and demonstrated duplicate prevention and automated publishing.

Previously processed topics were skipped, while new approved topics were published and stored in memory.

---

## Current Status

**Backend workflow: Operational and tested.**

The major backend pipeline is working end-to-end:

**Discovery → Scoring → Editorial Evaluation → Memory → Publishing → API Response**

The backend is ready to be integrated with the Echo Mind frontend.
