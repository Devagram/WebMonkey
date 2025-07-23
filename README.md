# WebMonkey Agent

## Overview
WebMonkey is a Python-based web automation agent designed to search for products, add them to a cart, and proceed to checkout on retail websites. It leverages Google ADK for agent orchestration and undetected-chromedriver with Selenium for robust browser automation, bypassing common anti-bot measures.

## Technology Stack
- **Python**: Main language for rapid prototyping and rich ecosystem.
- **Google ADK**: Agent orchestration, decision logic, and tool integration.
- **undetected-chromedriver & Selenium**: Browser automation, session management, and anti-bot bypass.
- **python-dotenv**: Loads environment variables for configuration.

## How to Run
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up environment variables**:
   - Create a `.env` file in `agents/web_agent/` with:
     ```
     PROJECT_ID=your_project_id
     REGION=your_region
     SERVICE_NAME=your_service_name
     PORT=your_port
     GOOGLE_API_KEY=your_google_api_key
     ```
3. **Run the agent**:
   - From the `agents` directory, start the agent using Google ADK:
     ```bash
     python -m web_agent.agent
     ```
   - The agent will launch a browser window for automation. Captchas are automatically solved; no manual intervention is required.

## Implementation Notes on Key Features

### Trajectory Maintenance
- The agent uses robust error handling in each tool (see `custom_tools.py`). If an action fails (e.g., page load, add to cart), errors are caught and logged, and the agent can retry or report the issue. Captchas are automatically solved, allowing the agent to continue toward the objective without losing session state.

### Objective Evaluation and Improvement
- The `metrics.py` module tracks each step's success, error, and time taken. After execution, metrics are analyzed to provide insights (success rate, error types, suggestions for improvement). This helps evaluate if the objective was met and how to optimize future runs.

### Dynamic Re-Planning
- The agent uses fuzzy matching (difflib) and modular logic to adapt if a product is unavailable or the UI changes. For example, if no exact product match is found, similar products are suggested. The agent can notify the user or adjust its actions based on real-time feedback from the site.

## Agent Workflow & Decision Logic
- **SearchAgent**: Finds products using search tools.
- **AddToCartAgent**: Adds the selected product to the cart.
- **CheckoutAgent**: Proceeds to checkout.
- **SequentialAgent**: Orchestrates the above steps in order.
- **Metrics**: Tracks success, errors, and performance for each step.

### Edge Case Handling
- Captchas and other manual steps are automatically handled by the agent. The session is reused for further automation.
- Errors are logged and analyzed; common issues are surfaced for improvement.

## Design Decisions
- **Session Reuse**: Manual steps (like captchas) are handled once, then the session is reused for seamless automation.
- **Minimal Imports**: Only necessary libraries are included for clarity and maintainability.
- **Tool-based Agents**: Each agent is focused on a single task for modularity and easier debugging.
