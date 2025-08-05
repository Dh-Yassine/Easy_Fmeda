import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import styles from "./Sidebar.module.css";

const navItems = [
  { label: "Home", path: "/", icon: "🏠" },
  { label: "Assumptions", path: "/assumptions", icon: "📋" },
  { label: "Safety Functions", path: "/safety-functions", icon: "⚡" },
  { label: "Components", path: "/components", icon: "🔧" },
  { label: "Failure Modes", path: "/failure-modes", icon: "🔍" },
  { label: "FMEDA Analysis", path: "/fmeda-analysis", icon: "📊" },
  { label: "Results", path: "/results", icon: "📈" },
];

export default function Sidebar() {
  const [hoveredItem, setHoveredItem] = useState(null);

  return (
    <aside className={styles.sidebar}>
      {/* Background blur effect */}
      <div className={styles["sidebar-backdrop"]} />

      {/* Header */}
      <div className={styles.header}>
        <div className={styles["logo-container"]}>
          <div className={styles.logo}>
            <span className={styles["logo-text"]}>F</span>
            <div className={styles["logo-glow"]} />
          </div>
          <div className={styles["brand-info"]}>
            <h1 className={styles.title}>FMEDA</h1>
            <span className={styles.subtitle}>Analysis Tool</span>
          </div>
        </div>
        <div className={styles["header-decoration"]} />
      </div>

      {/* Navigation */}
      <nav className={styles.nav}>
        {navItems.map((item, index) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              styles["nav-item"] + (isActive ? " " + styles.active : "")
            }
            onMouseEnter={() => setHoveredItem(index)}
            onMouseLeave={() => setHoveredItem(null)}
            end={item.path === "/"}
          >
            <div className={styles["nav-item-content"]}>
              <div className={styles["nav-icon"]}>
                <span className={styles.icon}>{item.icon}</span>
                <div className={styles["icon-glow"]} />
              </div>
              <span className={styles["nav-label"]}>{item.label}</span>
              <div className={styles["nav-ripple"]} />
            </div>
            {hoveredItem === index && (
              <div className={styles["hover-indicator"]} />
            )}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className={styles.footer}>
        <div className={styles["footer-content"]}>
          <div className={styles["footer-brand"]}>
            <span className={styles["footer-title"]}>Dhouibi</span>
            <span className={styles["footer-subtitle"]}>Professional Edition</span>
          </div>
          <div className={styles["footer-year"]}>© 2025</div>
        </div>
        <div className={styles["footer-decoration"]} />
      </div>
    </aside>
  );
}