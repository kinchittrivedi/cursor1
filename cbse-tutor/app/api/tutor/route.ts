import { NextRequest, NextResponse } from "next/server";

const SYSTEM_PROMPT = `You are an AI tutor for CBSE Class 8 students across Maths, Science, English, and Social Science. Explain in simple, age-appropriate language with step-by-step reasoning. When useful, include:
- Markdown lists and tables
- Mermaid diagrams using fenced code blocks like \n\n\`\`\`mermaid\nflowchart TD; A[Sunlight]-->B[Photosynthesis]\n\`\`\`\n\n- Simple chart blocks using: \n\n\`\`\`chart\n x: 1,2,3\n y: 2,4,3\n\`\`\`\n\nKeep answers concise and aligned with NCERT Class 8 syllabus. Avoid harmful or off-topic content.`;

interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const messages: ChatMessage[] = body?.messages ?? [];

  const apiKey = process.env.OPENAI_API_KEY;
  const userText = messages.filter((m) => m.role === "user").slice(-1)[0]?.content || "";

  if (!apiKey) {
    const mock = mockTutor(userText);
    return NextResponse.json({ text: mock });
  }

  try {
    const { OpenAI } = await import("openai");
    const client = new OpenAI({ apiKey });

    const chat = await client.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "system", content: SYSTEM_PROMPT }, ...messages],
      temperature: 0.6,
    });

    const text = chat.choices?.[0]?.message?.content ?? "Sorry, I could not generate a response.";
    return NextResponse.json({ text });
  } catch {
    return NextResponse.json({ text: "Sorry, the tutor is unavailable right now." }, { status: 200 });
  }
}

function mockTutor(input: string): string {
  const lower = (input || "").toLowerCase();
  if (lower.includes("photosynthesis")) {
    return `Photosynthesis is how green plants make food using sunlight, water, and carbon dioxide.

Key points:
- Chlorophyll in leaves absorbs sunlight
- Roots absorb water
- Leaves take in carbon dioxide from air
- Plants produce glucose (food) and release oxygen

\`\`\`mermaid
flowchart TD
  A[Sunlight] --> B[Chlorophyll in leaves]
  B --> C[Photosynthesis process]
  C --> D[Glucose (food)]
  C --> E[Oxygen released]
\`\`\`
`;
  }

  if (lower.includes("distance-time") || lower.includes("speed")) {
    return `Speed = Distance / Time. If a cyclist travels 20 km in 2 hours, speed = 10 km/h.

\`\`\`chart
x: 0,1,2,3,4
y: 0,5,10,15,20
\`\`\`
This chart shows distance increasing with time at constant speed.`;
  }

  return `Here is a simple explanation:
- Break the concept into smaller steps
- Understand key terms
- Practice with a small example
- Ask follow-up questions!
`;
}