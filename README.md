# Graspy AI

A multilingual educational platform for secondary school students in Nigeria powered by n-atlas model.

## Key Features

1. **Ask Questions**: Students can ask questions on any topic in **English** or any major **Nigerian language** (Yoruba, Hausa, Igbo, Pidgin).
2. **Multilingual Explanations**: Get comprehensive explanations in your preferred language.
3. **Interactive Chat**: Continue learning with an AI tutor to explore topics deeper.

---

## Project Structure

This project is a **monorepo** containing:

- **Frontend**: Next.js application running on port **3002**.
- **Backend**: Python FastAPI service running on port **8082**.

![Graspy Architecture](docs/graspy-architecture-natlas.png)

```bash
graspy/
├── apps/
│   ├── frontend/               # Next.js Frontend (Port 3002)
│   └── backend/                # Python Backend (Port 8082)
└── ...
```

---

## Local Setup

### Prerequisites

- Node.js & npm
- Python 3.12+
- `uv` (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/tosinamuda/graspy.git
   cd graspy
   ```

2. **Install dependencies** (Root)

   ```bash
   npm install
   ```

3. **Install Backend Dependencies**

   ```bash
   cd apps/backend
   uv sync
   cd ../..
   ```

4. **Configure Environment Variables**

   **Backend** (`apps/backend/.env`):

   ```bash
   cp apps/backend/.env.example apps/backend/.env
   # Edit .env and add your N-Atlas and Firebase private admin credentials
   ```

   **Frontend** (`apps/frontend/.env.local`):

   ```bash
   cp apps/frontend/.env.example apps/frontend/.env.local
   # Ensure NEXT_PUBLIC_API_URL=http://localhost:8082/api and add your firebase public credentials for authentication
   ```

5. **Run Database Setup**

   ```bash
   cd apps/backend
   uv run alembic upgrade head
   cd ../..
   ```

6. **Run the Application**
   ```bash
   npm run dev
   ```
   - **Frontend**: [http://localhost:3002](http://localhost:3002)
   - **Backend**: [http://localhost:8082](http://localhost:8082)

---

## Model Deployment

The AI model is deployed to **Modal**.

- **Deployment Guide**: [Read the full guide here](https://huggingface.co/tosinamuda/N-ATLaS-FP8/blob/main/deploy-guide.md)
- **Deployment Script**: `apps/model-deployment/modal_deploy_natlas-full.py`

> **Note**: You must create a secret for Hugging Face with your token before deploying.

---

## 📄 License

This project is licensed under the ISC License.
