# Architecture Documentation

## System Overview

The WWS Inventory Platform is built as a modern, cloud-native application with AI at its core. The architecture emphasizes scalability, maintainability, and developer experience.

## Architecture Principles

1. **Conversation-First**: Natural language is the primary interface
2. **AI-Native**: AI is integrated throughout, not bolted on
3. **API-First**: Everything accessible via REST/GraphQL APIs
4. **Event-Driven**: Async operations for scalability
5. **Multi-Tenant**: Designed for SaaS deployment from day one

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  Web (Next.js) │ Mobile (PWA) │ API Consumers               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
│  Load Balancer │ Rate Limiting │ Authentication             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   FastAPI    │  │  AI Engine   │  │   Workers    │      │
│  │   Services   │  │  (LangChain) │  │   (Celery)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       Data Layer                             │
│  PostgreSQL │ Redis │ Vector DB │ Elasticsearch             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   External Services                          │
│  OpenAI/Claude │ Email │ SMS │ Payment │ Logistics          │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (Next.js 14+)

**Technology Stack:**
- Next.js 14+ with App Router
- TypeScript for type safety
- Tailwind CSS + Shadcn/ui for styling
- React Query for state management
- Socket.io for real-time updates

**Key Features:**
- Server-Side Rendering (SSR) for SEO
- Progressive Web App (PWA) capabilities
- Optimistic UI updates
- Real-time chat interface
- Responsive design (mobile-first)

**Directory Structure:**
```
frontend/
├── src/
│   ├── app/              # Next.js 14 app directory
│   │   ├── (dashboard)/  # Dashboard routes
│   │   ├── (chat)/       # Chat interface routes
│   │   └── api/          # API routes (BFF pattern)
│   ├── components/       # React components
│   │   ├── ui/          # Base UI components
│   │   └── features/    # Feature-specific components
│   ├── lib/             # Utilities and helpers
│   ├── hooks/           # Custom React hooks
│   └── types/           # TypeScript definitions
```

### Backend (FastAPI)

**Technology Stack:**
- FastAPI for high-performance async API
- SQLAlchemy 2.0 for ORM
- Pydantic for data validation
- Celery for background tasks
- WebSocket for real-time features

**Key Features:**
- Automatic OpenAPI documentation
- Async request handling
- Database connection pooling
- Request/response validation
- Background job processing

**Directory Structure:**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/   # API endpoints
│   │       └── router.py    # Main router
│   ├── core/
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Database setup
│   │   └── security.py     # Auth & security
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── ai/                 # AI integration layer
```

### AI Engine (LangChain)

**Technology Stack:**
- LangChain for orchestration
- OpenAI GPT-4 / Anthropic Claude
- Pinecone for vector storage
- Custom fine-tuned models

**Architecture:**
```
AI Engine
├── Agents
│   ├── InventoryAgent      # Handles inventory queries
│   ├── OrderAgent          # Manages orders
│   ├── AnalyticsAgent      # Provides insights
│   └── GeneralAgent        # Routes to specialists
│
├── Tools
│   ├── InventoryTools      # Stock, products, warehouses
│   ├── OrderTools          # Order creation, tracking
│   ├── AnalyticsTools      # Reports, forecasts
│   └── IntegrationTools    # External system connectors
│
├── Memory
│   ├── ConversationBuffer  # Short-term context
│   ├── VectorMemory        # Long-term knowledge
│   └── UserPreferences     # Personalization
│
└── Prompts
    ├── SystemPrompts       # Role definitions
    ├── TaskPrompts         # Specific task templates
    └── FewShotExamples     # Training examples
```

**Agent Decision Flow:**
```
User Input
    ↓
Intent Classification
    ↓
Agent Selection
    ↓
Context Gathering
    ↓
Tool Selection & Execution
    ↓
Response Generation
    ↓
Learning & Feedback Loop
```

### Database Layer

**PostgreSQL with TimescaleDB:**
- Primary transactional database
- Time-series data for analytics
- Full-text search capabilities
- JSONB for flexible schemas

**Redis:**
- Session storage
- Cache layer
- Real-time pub/sub
- Rate limiting

**Vector Database (Pinecone):**
- Semantic search
- Product recommendations
- Document embeddings
- Conversation context

**Schema Design:**

```sql
-- Core Tables
products
├── id (PK)
├── sku (UNIQUE)
├── name, description
├── pricing, inventory
└── metadata (JSONB)

orders
├── id (PK)
├── order_number (UNIQUE)
├── customer info
├── financials
└── timestamps

order_items
├── id (PK)
├── order_id (FK)
├── product_id (FK)
└── line item details

-- AI Tables
conversations
├── id (PK)
├── session_id
├── user_id
└── metadata

conversation_messages
├── id (PK)
├── conversation_id (FK)
├── role, content
└── ai_metadata

ai_insights
├── id (PK)
├── type, priority
├── related_entity
└── lifecycle fields
```

## Data Flow

### Typical Request Flow

1. **User Action** (Frontend)
   - User types: "What's my stock for Product X?"

2. **API Request** (Frontend → Backend)
   - POST /api/v1/chat/message
   - Authenticated request with session token

3. **Request Validation** (Backend)
   - Pydantic schema validation
   - User authentication/authorization

4. **AI Processing** (AI Engine)
   - Intent classification: "stock_query"
   - Agent selection: InventoryAgent
   - Context gathering from DB
   - Tool execution: get_stock_levels("Product X")

5. **Database Query** (Backend)
   - SQL query to fetch product data
   - Cache check (Redis)
   - Cache update if needed

6. **Response Generation** (AI Engine)
   - Format data for human consumption
   - Add relevant suggestions
   - Include proactive insights

7. **Response Delivery** (Backend → Frontend)
   - JSON response with structured data
   - WebSocket push for real-time updates

8. **UI Update** (Frontend)
   - Optimistic update
   - Render response in chat
   - Update related dashboard widgets

### Background Job Flow

1. **Job Trigger**
   - Scheduled task (cron)
   - User action (async operation)
   - Event-driven (webhook)

2. **Job Queue** (Celery + Redis)
   - Task serialization
   - Priority assignment
   - Queue distribution

3. **Worker Processing**
   - Task execution
   - Error handling
   - Retry logic

4. **Result Storage**
   - Save to database
   - Update cache
   - Trigger notifications

## Security Architecture

### Authentication & Authorization

```
┌──────────────┐
│  User Login  │
└──────┬───────┘
       ↓
┌──────────────────┐
│  JWT Generation  │
│  (Access+Refresh)│
└──────┬───────────┘
       ↓
┌──────────────────┐
│  Token Storage   │
│  (HTTP-Only)     │
└──────┬───────────┘
       ↓
┌──────────────────┐
│  API Requests    │
│  (Bearer Token)  │
└──────┬───────────┘
       ↓
┌──────────────────┐
│  Verification    │
│  & RBAC Check    │
└──────────────────┘
```

**Security Measures:**
- JWT-based authentication
- Role-Based Access Control (RBAC)
- API rate limiting
- SQL injection prevention (ORM)
- XSS protection
- CSRF tokens
- HTTPS only
- Environment-based secrets

### Data Privacy

- PII encryption at rest
- Data anonymization for analytics
- GDPR compliance features
- Right to be forgotten
- Data export capabilities
- Audit logging

## Scalability Strategy

### Horizontal Scaling

**Application Layer:**
- Stateless API servers
- Load balancer distribution
- Auto-scaling based on metrics

**Database Layer:**
- Read replicas for queries
- Write to primary only
- Connection pooling
- Query optimization

**Cache Layer:**
- Redis cluster mode
- Cache invalidation strategy
- Distributed caching

### Performance Optimization

**Frontend:**
- Code splitting
- Lazy loading
- Image optimization
- CDN for static assets

**Backend:**
- Database indexing
- Query optimization
- Async operations
- Response compression

**AI:**
- Prompt caching
- Response streaming
- Model selection by task
- Token optimization

## Monitoring & Observability

### Metrics

**Application Metrics:**
- Request rate, latency, errors
- Database query performance
- Cache hit rates
- AI token usage

**Business Metrics:**
- Active users (DAU/MAU)
- Feature adoption
- Conversation success rate
- Cost per conversation

### Logging

```
Log Levels:
- ERROR: System failures
- WARN: Degraded performance
- INFO: Business events
- DEBUG: Detailed diagnostics

Log Aggregation:
ELK Stack (Elasticsearch, Logstash, Kibana)
```

### Alerting

- Error rate thresholds
- Latency degradation
- Database connection issues
- High AI costs
- Security events

## Deployment

### Containerization

```
Docker Images:
├── wws-frontend    # Next.js app
├── wws-backend     # FastAPI app
├── wws-worker      # Celery workers
└── wws-nginx       # Reverse proxy
```

### Orchestration (Kubernetes)

```
Kubernetes Resources:
├── Deployments
│   ├── frontend (3 replicas)
│   ├── backend (5 replicas)
│   └── workers (2 replicas)
├── Services
│   ├── LoadBalancer (frontend)
│   └── ClusterIP (backend)
├── ConfigMaps & Secrets
└── Ingress (SSL/TLS)
```

### CI/CD Pipeline

```
Git Push
    ↓
GitHub Actions
    ↓
├─→ Lint & Test
├─→ Build Images
├─→ Security Scan
└─→ Deploy to Staging
    ↓
Manual Approval
    ↓
Deploy to Production
    ↓
Health Checks
    ↓
Rollback if Needed
```

## Future Architecture Considerations

### Phase 2 Enhancements

- GraphQL API alongside REST
- Event sourcing for audit trail
- CQRS pattern for complex domains
- Microservices extraction (if needed)
- Multi-region deployment
- Edge computing for global users

### Advanced AI Features

- Fine-tuned domain models
- Reinforcement learning from user feedback
- Automated workflow discovery
- Predictive analytics
- Computer vision for product recognition
- Voice interface

## Technology Decisions

### Why Next.js?
- Best-in-class React framework
- Excellent DX and performance
- Built-in optimizations
- Server components for faster loads

### Why FastAPI?
- Modern Python framework
- Async by default
- Auto-generated docs
- Better AI/ML integration than Django

### Why LangChain?
- De facto standard for LLM apps
- Rich ecosystem of tools
- Active development
- Multi-LLM support

### Why PostgreSQL?
- Robust and reliable
- JSONB for flexibility
- Excellent extension ecosystem
- TimescaleDB for time-series

## Conclusion

This architecture balances:
- **Performance**: Async ops, caching, optimizations
- **Scalability**: Horizontal scaling, stateless design
- **Maintainability**: Clear separation of concerns
- **Developer Experience**: Modern tools, good docs
- **User Experience**: Fast, intuitive, AI-powered

The system is designed to evolve with needs while maintaining core principles of simplicity and conversation-first interaction.
