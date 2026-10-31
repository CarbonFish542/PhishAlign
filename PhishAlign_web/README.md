# PhishAlign

Frontend for **Cross-Modal Consistency-Based Phishing Website Detection**.

This is a React research-prototype UI. Analysis results currently come from mock data in `src/data/mockResults.ts` through `src/services/api.ts`. Replace those service functions with FastAPI calls later.

## Run

```bash
cd PhishAlgin
npm install
npm run dev
```

Open http://localhost:5173/

## Routes

- `/` — landing and URL analysis
- `/analyze` — processing pipeline
- `/results` — classification dashboard
- `/about` — methodology

Use **Phishing demo** and **Legitimate demo** on the home page. Enable **Research Mode** on the results page to compare conventional multimodal fusion with consistency-aware fusion.
