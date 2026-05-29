"use client";

import { useState } from "react";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { Input } from "../components/Input";
import { ProgressBar } from "../components/ProgressBar";

export default function Home() {
  const [progress, setProgress] = useState(0);
  const [isTranslating, setIsTranslating] = useState(false);

  const handleTranslate = () => {
    setIsTranslating(true);
    setProgress(10);
    
    // Simulate translation progress
    const interval = setInterval(() => {
      setProgress(p => {
        if (p >= 100) {
          clearInterval(interval);
          setIsTranslating(false);
          return 100;
        }
        return p + 10;
      });
    }, 500);
  };

  return (
    <main style={{ padding: "40px 20px", maxWidth: "800px", margin: "0 auto" }}>
      <header style={{ textAlign: "center", marginBottom: "40px" }} className="fade-in">
        <h1 className="heading-gradient" style={{ fontSize: "3rem", marginBottom: "16px" }}>🌐💬 Aphra</h1>
        <p style={{ color: "hsl(var(--text-secondary))", fontSize: "1.125rem" }}>
          Translate whole books with open-source models.
        </p>
      </header>

      <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
        <Card>
          <h2>Configuration</h2>
          <Input label="OpenRouter API Key" type="password" placeholder="sk-or-v1-..." />
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginTop: "16px" }}>
            <Input label="Source Language" placeholder="e.g. English" defaultValue="English" />
            <Input label="Target Language" placeholder="e.g. French" defaultValue="French" />
          </div>
        </Card>

        <Card>
          <h2>Document Upload</h2>
          <div style={{ 
            border: "2px dashed hsl(var(--border-color))", 
            padding: "40px", 
            borderRadius: "var(--radius-sm)",
            textAlign: "center",
            cursor: "pointer",
            marginTop: "8px"
          }} className="hover-lift">
            <p style={{ color: "hsl(var(--text-secondary))" }}>Click to upload .epub or .md files</p>
          </div>
        </Card>

        <Button onClick={handleTranslate} disabled={isTranslating} style={{ width: "100%", padding: "16px", fontSize: "1.125rem" }}>
          {isTranslating ? "Translating..." : "Start Translation"}
        </Button>

        {isTranslating && (
          <Card>
            <ProgressBar progress={progress} label="Translation Progress" />
          </Card>
        )}
      </div>
    </main>
  );
}
