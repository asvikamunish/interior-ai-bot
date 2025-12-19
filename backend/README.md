# Conversational AI – Interior Design WhatsApp Bot (Mock)

## Overview
This project is a conversational AI system designed to simulate a human-like interior design consultation experience. The chatbot understands user requirements, asks intelligent follow-up questions, remembers past conversations, and resumes context across sessions. An Admin Dashboard is provided to monitor conversations in real time.

The system is built using FastAPI and a Large Language Model (Groq – LLaMA 3.1), with a modular architecture that supports easy replacement of the LLM provider.

---

## Key Features

### 1. Conversational AI (Interior Designer Persona)
- AI persona named **Aira**, a professional interior designer
- Natural, polite, and structured responses
- Asks clarifying questions when user input is incomplete
- Provides realistic and practical design suggestions

### 2. Session & Context Management (Critical)
- Each user is identified using a `session_id`
- Conversation history is preserved per session
- Context such as:
  - Room type
  - Budget
  - Style preference  
  is automatically extracted and stored
- Conversations resume seamlessly across multiple messages

### 3. Context-Aware AI Responses
- Extracted context is dynamically injected into the LLM prompt
- AI responses reference previously discussed details
- Enables personalized and continuous conversations

### 4. Admin Dashboard (Mandatory Requirement)
- View all active user sessions
- Inspect extracted context for each user
- View complete conversation history
- Track last active timestamps
- Simple web-based dashboard served via FastAPI

### 5. WhatsApp Integration
- A mock WhatsApp-style interaction is implemented using a REST API
- The system architecture supports real WhatsApp integration via Twilio

---

## Tech Stack

- **Backend**: FastAPI (Python)
- **LLM Provider**: Groq (LLaMA 3.1 – 8B Instant)
- **Environment Management**: python-dotenv
- **Admin Dashboard**: HTML + JavaScript
- **Session Storage**: In-memory (dictionary-based)

---

## Architecture Overview

