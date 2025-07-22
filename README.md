# WebMonkey Cloud Run Application

WebMonkey is a Google ADK Agent-based Cloud Run application designed to seamlessly deploy intelligent agents in a serverless environment. This repository contains the code and configuration needed to build, deploy, and manage your agent on Google Cloud Run.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Building and Running Locally](#building-and-running-locally)
- [Deployment to Cloud Run](#deployment-to-cloud-run)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project leverages the Google Agent Development Kit (ADK) to build a cloud-native agent that can be served via Google Cloud Run. The agent can process requests, make decisions, and return responses based on your custom logic.

## Prerequisites

- Google Cloud SDK (gcloud) installed and initialized
- Docker installed (for local builds)
- A Google Cloud project with billing enabled
- IAM permissions to deploy to Cloud Run
- Google ADK SDK dependencies (see `requirements.txt` or `package.json`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/webmonkey.git
   cd webmonkey
   ```

2. Install dependencies (Python example):
   ```bash
   pip install -r requirements.txt
   ```

   Or for Node.js:
   ```bash
   npm install
   ```

## Configuration

Before deploying, configure the following environment variables:

- `PROJECT_ID` – Your Google Cloud project ID
- `REGION` – Desired Cloud Run region (e.g., `us-central1`)
- `SERVICE_NAME` – Name of the Cloud Run service

You can set these in your shell or via a `.env` file.

## Building and Running Locally

1. Build the Docker image:
   ```bash
   docker build -t gcr.io/$PROJECT_ID/webmonkey-agent:latest .
   ```

2. Run the container locally:
   ```bash
   docker run -p 8080:8080 \
     -e PROJECT_ID=$PROJECT_ID \
     -e REGION=$REGION \
     -e SERVICE_NAME=$SERVICE_NAME \
     gcr.io/$PROJECT_ID/webmonkey-agent:latest
   ```

3. Test the endpoint:
   ```bash
   curl http://localhost:8080/agent-endpoint
   ```

## Deployment to Cloud Run

1. Submit the build to Google Container Registry:
   ```bash
   docker push gcr.io/$PROJECT_ID/webmonkey-agent:latest
   ```

2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy $SERVICE_NAME \
     --image gcr.io/$PROJECT_ID/webmonkey-agent:latest \
     --region $REGION \
     --platform managed \
     --allow-unauthenticated
   ```

3. After deployment, note the service URL and test:
   ```bash
   curl https://$SERVICE_NAME-$REGION.a.run.app/agent-endpoint
   ```

## Usage

Send HTTP POST requests to the `/agent-endpoint` with a JSON payload describing the task for the agent. Example:

```json
{
  "input": "Perform X analysis",
  "parameters": { /* custom parameters */ }
}
```

The service will return a JSON response with the agent's decision or output.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for bug fixes and enhancements.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

