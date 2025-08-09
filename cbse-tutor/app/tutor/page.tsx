"use client";

import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import mermaid from "mermaid";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

function MermaidBlock({ code }: { code: string }) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    mermaid.initialize({ startOnLoad: false, theme: "default" });
    const id = `mmd-${Math.random().toString(36).slice(2)}`;
    const render = async () => {
      try {
        const { svg } = await mermaid.render(id, code);
        if (containerRef.current) {
          containerRef.current.innerHTML = svg;
        }
      } catch {
        if (containerRef.current) {
          containerRef.current.textContent = "Mermaid render error";
        }
      }
    };
    render();
  }, [code]);

  return <div ref={containerRef} />;
}

export default function TutorPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Hi! I am your Class 8 AI tutor. Ask me about Maths, Science, English, or Social Science. Try: 'Explain photosynthesis with a diagram'.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function sendMessage() {
    if (!input.trim()) return;
    const userMessage: ChatMessage = { role: "user", content: input };
    const nextMessages: ChatMessage[] = [...messages, userMessage];
    setMessages(nextMessages);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("/api/tutor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: nextMessages }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data.text }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I had trouble responding. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  function renderBlock(content: string) {
    // naive detection for mermaid and chart examples
    if (content.trim().startsWith("```mermaid")) {
      const code = content.replace(/^```mermaid\n/, "").replace(/```\s*$/, "");
      return <MermaidBlock code={code} />;
    }

    if (content.trim().startsWith("```chart")) {
      // Example chart block
      // ```chart
      // x: 1,2,3,4
      // y: 2,4,1,5
      // ```
      const lines = content
        .replace(/^```chart\n/, "")
        .replace(/```\s*$/, "")
        .split(/\n/)
        .map((l) => l.trim());
      const xLine = lines.find((l) => l.startsWith("x:")) || "x:";
      const yLine = lines.find((l) => l.startsWith("y:")) || "y:";
      const xs = xLine.replace("x:", "").split(",").map((s) => s.trim());
      const ys = yLine
        .replace("y:", "")
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n));

      return (
        <Line
          data={{
            labels: xs,
            datasets: [
              {
                label: "Values",
                data: ys,
                borderColor: "#2563eb",
              },
            ],
          }}
          options={{ responsive: true, plugins: { legend: { display: true } } }}
        />
      );
    }

    return <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>;
  }

  return (
    <div>
      <h2>AI Tutor</h2>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 12,
          border: "1px solid #e5e7eb",
          padding: 12,
          borderRadius: 8,
          minHeight: 300,
        }}
      >
        {messages.map((m, idx) => (
          <div key={idx} style={{ background: m.role === "assistant" ? "#f8fafc" : "#fff" }}>
            <div style={{ fontSize: 12, color: "#6b7280" }}>{m.role}</div>
            {renderBlock(m.content)}
          </div>
        ))}
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          sendMessage();
        }}
        style={{ display: "flex", gap: 8, marginTop: 12 }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about a topic..."
          style={{ flex: 1, padding: 8, border: "1px solid #e5e7eb", borderRadius: 8 }}
        />
        <button
          type="submit"
          disabled={isLoading}
          style={{ padding: "8px 12px", borderRadius: 8, background: "#111827", color: "#fff" }}
        >
          {isLoading ? "Thinking..." : "Send"}
        </button>
      </form>

      <div style={{ marginTop: 16, fontSize: 12, color: "#6b7280" }}>
        Tips: Ask for diagrams using mermaid by saying &quot;Draw a mermaid diagram of water cycle&quot; or ask for a chart with values.
      </div>
    </div>
  );
}