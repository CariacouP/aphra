import React from "react";
import styles from "./ProgressBar.module.css";

interface ProgressBarProps {
  progress: number;
  label?: string;
}

export function ProgressBar({ progress, label }: ProgressBarProps) {
  return (
    <div className={styles.wrapper}>
      {label && <div className={styles.label}>{label} <span>{Math.round(progress)}%</span></div>}
      <div className={styles.track}>
        <div 
          className={styles.fill} 
          style={{ width: `${Math.min(Math.max(progress, 0), 100)}%` }}
        />
      </div>
    </div>
  );
}
