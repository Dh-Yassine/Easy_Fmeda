import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./SafetyFunctions.module.css";
import {
  getSafetyFunctions,
  createSafetyFunction,
  updateSafetyFunction,
  deleteSafetyFunction,
} from "../../api/fmedaApi";

const ASIL_LEVELS = [
  { value: "ASIL A", label: "ASIL A", description: "Lowest safety integrity level", color: "#4caf50" },
  { value: "ASIL B", label: "ASIL B", description: "Low safety integrity level", color: "#ff9800" },
  { value: "ASIL C", label: "ASIL C", description: "High safety integrity level", color: "#f44336" },
  { value: "ASIL D", label: "ASIL D", description: "Highest safety integrity level", color: "#9c27b0" }
];

export default function SafetyFunctions({ currentProject }) {
  const [safetyFunctions, setSafetyFunctions] = useState([]);
  const [form, setForm] = useState({ sf_id: "", description: "", target_integrity_level: ASIL_LEVELS[0].value });
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  // Load safety functions for current project
  useEffect(() => {
    if (currentProject) {
      loadSafetyFunctions();
    }
  }, [currentProject]);

  const loadSafetyFunctions = async () => {
    if (!currentProject) return;
    
    try {
      const data = await getSafetyFunctions(currentProject.id);
      setSafetyFunctions(data);
    } catch (error) {
      console.error("Failed to load safety functions:", error);
      setError("Failed to load safety functions.");
    }
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!currentProject) {
      setError("No project selected. Please create or load a project first.");
      return;
    }

    if (!form.sf_id.trim() || !form.description.trim()) {
      setError("ID and Description are required.");
      return;
    }

    setIsLoading(true);
    setError("");
    
    try {
      if (editingId) {
        await updateSafetyFunction(editingId, form);
      } else {
        await createSafetyFunction({
          ...form,
          project: currentProject.id
        });
      }
      setForm({ sf_id: "", description: "", target_integrity_level: ASIL_LEVELS[0].value });
      setEditingId(null);
      await loadSafetyFunctions();
    } catch (error) {
      setError("Failed to save safety function. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (sf) => {
    setForm({
      sf_id: sf.sf_id,
      description: sf.description,
      target_integrity_level: sf.target_integrity_level,
    });
    setEditingId(sf.id);
  };

  const handleDelete = async (sfId) => {
    if (window.confirm("Delete this Safety Function?")) {
      try {
        await deleteSafetyFunction(sfId);
        await loadSafetyFunctions();
      } catch (error) {
        setError("Failed to delete safety function.");
      }
    }
  };

  const handleContinue = () => {
    if (safetyFunctions.length > 0) {
      navigate("/components");
    } else {
      alert("Please add at least one Safety Function before continuing.");
    }
  };

  const getAsilColor = (level) => {
    const asil = ASIL_LEVELS.find(a => a.value === level);
    return asil ? asil.color : "#666";
  };

  if (!currentProject) {
    return (
      <div className={styles.noProject}>
        <h2>No Project Selected</h2>
        <p>Please create or load a project first to manage Safety Functions.</p>
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
    <div className={styles.container}>
      <div className={styles.backdrop}></div>
      
      <div className={styles.header}>
        <h2>Safety Functions</h2>
        <p className={styles.projectInfo}>
          Project: <span className={styles.projectName}>{currentProject.name}</span>
        </p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label className={styles.label}>
              <span className={styles.labelIcon}>🆔</span>
              Safety Function ID
            </label>
            <input
              name="sf_id"
              placeholder="e.g., SF001, SF002, SF_MAIN"
              value={form.sf_id}
              onChange={handleChange}
              className={styles.input}
              required
            />
            <p className={styles.helpText}>Enter a unique identifier for this safety function</p>
          </div>
        </div>

        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label className={styles.label}>
              <span className={styles.labelIcon}>🎯</span>
              Target Integrity Level
            </label>
            <div className={styles.asilSelector}>
              {ASIL_LEVELS.map((level) => (
                <label key={level.value} className={styles.asilOption}>
                  <input
                    type="radio"
                    name="target_integrity_level"
                    value={level.value}
                    checked={form.target_integrity_level === level.value}
                    onChange={handleChange}
                    className={styles.asilRadio}
                  />
                  <div 
                    className={styles.asilCard}
                    style={{ borderColor: getAsilColor(level.value) }}
                  >
                    <div className={styles.asilLabel}>{level.label}</div>
                    <div className={styles.asilDescription}>{level.description}</div>
                  </div>
                </label>
              ))}
            </div>
          </div>
        </div>
        
        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label className={styles.label}>
              <span className={styles.labelIcon}>📝</span>
              Description
            </label>
            <textarea
              name="description"
              placeholder="Describe the safety function, its purpose, and requirements. Be specific about what this safety function protects against..."
              value={form.description}
              onChange={handleChange}
              className={styles.textarea}
              required
              rows="4"
            />
            <p className={styles.helpText}>Provide a detailed description of the safety function and its requirements</p>
          </div>
        </div>

        <div className={styles.formActions}>
          <button 
            className={styles.saveBtn} 
            type="submit"
            disabled={isLoading}
          >
            <span className={styles.btnIcon}>
              {isLoading ? "⏳" : (editingId ? "✏️" : "➕")}
            </span>
            <span>
              {isLoading ? "Saving..." : (editingId ? "Update Safety Function" : "Add Safety Function")}
            </span>
          </button>
          
          {editingId && (
            <button
              type="button"
              className={styles.cancelBtn}
              onClick={() => {
                setForm({ sf_id: "", description: "", target_integrity_level: ASIL_LEVELS[0].value });
                setEditingId(null);
              }}
            >
              <span className={styles.btnIcon}>❌</span>
              <span>Cancel</span>
            </button>
          )}
        </div>
      </form>

      {error && <div className={styles.error}>{error}</div>}

      <div className={styles.tableSection}>
        <div className={styles.tableHeader}>
          <h3>Safety Functions ({safetyFunctions.length})</h3>
          {safetyFunctions.length > 0 && (
            <button 
              className={styles.continueBtn} 
              onClick={handleContinue}
            >
              <span className={styles.btnIcon}>🚀</span>
              <span>Continue to Components</span>
              <span className={styles.btnArrow}>→</span>
            </button>
          )}
        </div>

        {safetyFunctions.length === 0 ? (
          <div className={styles.emptyState}>
            <div className={styles.emptyIcon}>📋</div>
            <h4>No Safety Functions Defined</h4>
            <p>Add your first Safety Function above to get started with your FMEDA analysis.</p>
            <p>Safety Functions define the critical safety requirements that your system must meet.</p>
          </div>
        ) : (
          <table className={styles.table}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Description</th>
                <th>ASIL Level</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {safetyFunctions.map((sf) => (
                <tr key={sf.id}>
                  <td className={styles.sfId}>{sf.sf_id}</td>
                  <td className={styles.description}>{sf.description}</td>
                  <td className={styles.asil}>
                    <span 
                      className={styles.asilBadge}
                      style={{ backgroundColor: getAsilColor(sf.target_integrity_level) }}
                    >
                      {sf.target_integrity_level}
                    </span>
                  </td>
                  <td className={styles.actions}>
                    <button className={styles.editBtn} onClick={() => handleEdit(sf)}>
                      <span className={styles.btnIcon}>✏️</span>
                      <span>Edit</span>
                    </button>
                    <button className={styles.deleteBtn} onClick={() => handleDelete(sf.id)}>
                      <span className={styles.btnIcon}>🗑️</span>
                      <span>Delete</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
