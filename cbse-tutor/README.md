# CBSE Class 8 AI Tutor (Prototype)

Local prototype for a subscription-gated AI tutor focused on CBSE Class 8.

## Features
- Landing page with CTA
- Mock subscription flow (cookie-based)
- Tutor chat with Markdown, Mermaid diagrams, and simple charts
- API integrates with OpenAI when `OPENAI_API_KEY` is provided; otherwise uses mock responses

## Run locally
```bash
npm install
npm run dev
```
Then open http://localhost:3000

To enable real AI responses, set an environment variable before running:
```bash
export OPENAI_API_KEY=your_key_here
npm run dev
```

## Tips
- Ask for diagrams: "Draw a mermaid diagram of the water cycle."
- Ask for charts: "Show a distance-time chart for constant speed 5 km/h for 0 to 4 hours."

## License
For internal prototyping only.
