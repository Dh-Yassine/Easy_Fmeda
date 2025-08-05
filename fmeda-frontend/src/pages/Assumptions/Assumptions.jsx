import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Assumptions.module.css";
import { updateProject } from "../../api/fmedaApi";

export default function Assumptions({ currentProject, setCurrentProject }) {
  const [lifetime, setLifetime] = useState("");
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  // Set lifetime from current project if available
  useEffect(() => {
    if (currentProject) {
      setLifetime(currentProject.lifetime?.toString() || "");
    }
  }, [currentProject]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!currentProject) {
      alert("No project selected. Please create a project first.");
      return;
    }

    if (!lifetime || lifetime <= 0) {
      alert("Please enter a valid system lifetime (greater than 0).");
      return;
    }

    setIsLoading(true);
    try {
      const updatedProject = await updateProject(currentProject.id, { lifetime: Number(lifetime) });
      setCurrentProject(updatedProject);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 2000);
    } catch (error) {
      alert("Failed to update system lifetime. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleContinue = () => {
    if (currentProject && currentProject.lifetime > 0) {
      navigate("/safety-functions");
    } else {
      alert("Please set the system lifetime before continuing.");
    }
  };

  if (!currentProject) {
    return (
      <div className={styles.noProject}>
        <h2>No Project Selected</h2>
        <p>Please create or load a project first to set analysis assumptions.</p>
        <button 
          className={styles.backBtn} 
          onClick={() => navigate("/")}
        >
          ← Back to Home
        </button>
      </div>
    );
  }

  return (
    <div style={{ width: "100%", margin: 0, padding: 0, background: "#f6f7fb", minHeight: "100vh" }}>
      <div className={styles.assumptions}>
        <div className={styles.header}>
          <h2>Analysis Assumptions</h2>
          <p className={styles.projectInfo}>
            Project: <span className={styles.projectName}>{currentProject.name}</span>
          </p>
        </div>

        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label className={styles.label}>
              System Lifetime (hours):
              <input
                type="number"
                min="1"
                step="1"
                value={lifetime}
                onChange={(e) => setLifetime(e.target.value)}
                className={styles.input}
                placeholder="Enter system lifetime in hours"
                required
              />
            </label>
            <p className={styles.helpText}>
              The system lifetime is used to calculate Mean Probability of Hazardous Failure (MPHF).
            </p>
          </div>

          <div className={styles.actions}>
            <button 
              className={styles.saveBtn} 
              type="submit"
              disabled={isLoading}
            >
              {isLoading ? "Saving..." : "💾 Save Lifetime"}
            </button>
            
            {currentProject.lifetime > 0 && (
              <button 
                className={styles.continueBtn} 
                type="button"
                onClick={handleContinue}
              >
                🚀 Continue to Safety Functions →
              </button>
            )}
          </div>

          {success && (
            <div className={styles.success}>
              ✅ System lifetime saved successfully!
            </div>
          )}
        </form>

        <div className={styles.info}>
          <h3>About System Lifetime</h3>
          <p>
            The system lifetime is a critical parameter for FMEDA calculations. It represents 
            the total operating time of the system and is used to calculate the Mean Probability 
            of Hazardous Failure (MPHF) metric.
          </p>
          <ul>
            <li><strong>Typical values:</strong> 10,000 to 100,000 hours</li>
            <li><strong>Automotive applications:</strong> 15,000 to 20,000 hours</li>
            <li><strong>Industrial applications:</strong> 50,000 to 100,000 hours</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
