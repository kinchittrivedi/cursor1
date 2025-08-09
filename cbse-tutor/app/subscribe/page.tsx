"use client";

import { useState } from "react";

export default function SubscribePage() {
  const [status, setStatus] = useState<string>("");

  async function subscribe() {
    // Mock: set cookie via API route
    const res = await fetch("/api/subscription", { method: "POST" });
    if (res.ok) {
      setStatus("Subscribed! You can now access the tutor.");
    } else {
      setStatus("Subscription failed. Try again.");
    }
  }

  return (
    <div>
      <h2>Subscribe</h2>
      <p>Unlock full access to the Class 8 AI Tutor.</p>
      <button onClick={subscribe} style={{ padding: "8px 12px", borderRadius: 8 }}>
        Subscribe (Mock)
      </button>
      <div style={{ marginTop: 8 }}>{status}</div>
    </div>
  );
}