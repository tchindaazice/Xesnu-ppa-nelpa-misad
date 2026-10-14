# VPN Platform - Specification v2

This monorepo contains the code for a professional, multi-role VPN Platform designed specifically for the African market (Mobile Money integration, WhatsApp/Telegram onboarding). The platform is built using Xray-core, Marzban, FastAPI, React, and Flutter.

## Architecture & Components

The system is split into four main components:
- **gateway/**: The core backend ("Le service client et la caisse"). Built with Python 3.12, FastAPI, PostgreSQL 16, and Redis 7. It handles users, wallets, payments, role-based access control (RBAC), and interacts with Marzban.
- **panel/**: The Web Panel for Super Admins, Admins, and Resellers. Built with React, Vite, TypeScript, and Tailwind.
- **mobile/**: The user-facing mobile application. Built with Flutter, connecting via VLESS-WS.
- **infra/**: Infrastructure definitions using Docker Compose. Includes configurations for PostgreSQL, Redis, Marzban, Nginx, and the backend/frontend services.
- **docs/**: Project documentation, ADRs (Architecture Decision Records), and runbooks.

## Getting Started (Local Development)

1. **Environment Variables**:
   Copy `.env.example` to `.env` inside the `infra/` folder.
   ```bash
   cp infra/.env.example infra/.env
   # Update passwords and secrets in infra/.env
   ```

2. **Start the Infrastructure**:
   Use Docker Compose to spin up the entire stack:
   ```bash
   cd infra
   docker-compose up -d
   ```
   This will start:
   - PostgreSQL 16 (port 5432)
   - Redis 7 (port 6379)
   - Marzban (host network)
   - Nginx (Reverse proxy for `/vless-ws`)
   - Gateway API (port 8080)
   - Web Panel (port 8081)

3. **Running Gateway Tests**:
   The `gateway/` service uses `pytest`. Ensure you are in the gateway directory, export the required dummy environment variables, and run:
   ```bash
   cd gateway
   pip install -r requirements.txt
   export POSTGRES_PASSWORD=test JWT_SIGNING_KEY=test MARZBAN_API_USER=test MARZBAN_API_PASSWORD=test
   PYTHONPATH=. pytest tests/
   ```

## Workflow & Guidelines

- **Branches & Commits**: Create one pull request per task (e.g., `feat/T-101`). Include tests.
- **Secrets**: NEVER commit secrets. Use `.env`.
- **RBAC & Audit**: All admin endpoints must enforce RBAC and write to the audit log.
- **VPN Engine**: Do not query Marzban directly. Use the `VpnEngineClient` abstraction.
