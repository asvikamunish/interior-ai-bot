Interior Design Conversational AI Bot

This project implements a conversational AI system for an interior design consultation use case, built with a focus on real-time observability.

The backend is developed using FastAPI. FastAPI handles all API endpoints including chat interactions, session lifecycle management, and admin-level inspection APIs.

LLM integration is handled using the Groq API. The LLM is used strictly for response generation, while conversation state and contextual memory are managed explicitly at the application layer. This separation ensures predictable behavior and allows context to persist beyond a single prompt-response cycle. A system prompt defines the interior designer persona, tone, and response constraints.

Session management is implemented using server-side session storage keyed by a session_id. Each session stores structured conversation history, extracted context (such as room type, style preferences, and budget indicators), and metadata including message count and last activity timestamp. 

A mock WhatsApp-style chat interface is implemented using plain HTML, CSS, and JavaScript. This frontend communicates with the backend via REST calls and simulates real-world messaging behavior using session identifiers similar to phone numbers. 

This approach demonstrates the system’s readiness for WhatsApp integration without introducing external dependencies such as Twilio during development.

An admin dashboard is provided to observe system behavior in real time. It consumes backend admin APIs to display active sessions, conversation history, extracted context, and session activity data. This allows monitoring, debugging, and evaluation of conversation quality and system performance.

Tooling and technologies used:

FastAPI for backend API design and request handling

Groq API for LLM-based response generation

Python for session logic, context extraction, and orchestration

HTML, CSS, and JavaScript for mock chat UI and admin dashboard

Render for deployment and environment configuration

The overall architecture separates conversation intelligence, session state, and presentation layers, enabling maintainability, extensibility, and clear evaluation of conversational behavior.