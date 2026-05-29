import React from "react";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export function Card({ children, className, ...props }: CardProps) {
  return (
    <div
      className={`glass-container fade-in ${className || ""}`}
      style={{ padding: "24px", display: "flex", flexDirection: "column", gap: "16px" }}
      {...props}
    >
      {children}
    </div>
  );
}
