from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from agents.web_agent.metrics import metrics_tracker

app = FastAPI()

@app.get('/metrics', response_class=HTMLResponse)
def show_metrics():
    analysis = metrics_tracker.analyze()
    insights = analysis["insights"]
    suggestions = analysis["suggestions"]
    html = f"""
    <h1>Objective Metrics Analysis</h1>
    <h2>Insights</h2>
    <ul>
        <li>Success Rate: {insights['success_rate']:.2f}</li>
        <li>Average Time Taken: {insights['average_time_taken']:.2f} seconds</li>
        <li>Error Recovery Efficiency: {insights['error_recovery_efficiency']:.2f}</li>
        <li>Common Errors: {', '.join(insights['common_errors'].keys()) if insights['common_errors'] else 'None'}</li>
    </ul>
    <h2>Suggestions</h2>
    <ul>
        {''.join(f'<li>{s}</li>' for s in suggestions) if suggestions else '<li>No suggestions. Performance is optimal.</li>'}
    </ul>
    """
    return HTMLResponse(content=html)

# To run: uvicorn agents.web_metrics_server:app --host 0.0.0.0 --port 5000

