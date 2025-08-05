import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import styles from "./FailureModes.module.css";
import { 
  getFailureModes, 
  createFailureMode, 
  updateFailureMode, 
  deleteFailureMode,
  getComponents 
} from "../../api/fmedaApi";

export default function FailureModes({ currentProject }) {
  const [failureModes, setFailureModes] = useState([]);
  const [components, setComponents] = useState([]);
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [currentComponent, setCurrentComponent] = useState(null);
  const [form, setForm] = useState({
    description: "",
    failure_rate_total: "",
    system_level_effect: "",
    is_SPF: false,
    is_MPF: false,
    SPF_safety_mechanism: "",
    SPF_diagnostic_coverage: "",
    MPF_safety_mechanism: "",
    MPF_diagnostic_coverage: "",
    component: null
  });
  const [error, setError] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { componentId } = useParams();

  // Load components and failure modes for current project
  useEffect(() => {
    if (currentProject) {
      loadComponents();
      if (componentId) {
        setSelectedComponent(componentId);
        loadFailureModes(componentId);
      }
    }
  }, [currentProject, componentId]);

  const loadComponents = async () => {
    if (!currentProject) return;
    
    try {
      const data = await getComponents(currentProject.id);
      setComponents(data);
    } catch (error) {
      console.error("Failed to load components:", error);
      setError("Failed to load components.");
    }
  };

  const loadFailureModes = async (compId) => {
    if (!compId) return;
    
    try {
      console.log(`Loading failure modes for component ID: ${compId}`);
      const data = await getFailureModes(compId);
      console.log(`Received failure modes data:`, data);
      setFailureModes(data);
    } catch (error) {
      console.error("Failed to load failure modes:", error);
      setError("Failed to load failure modes.");
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleComponentChange = (e) => {
    const compId = e.target.value;
    setSelectedComponent(compId);
    setForm(prev => ({ ...prev, component: compId }));
    
    const selectedComp = components.find(c => c.id == compId);
    setCurrentComponent(selectedComp);
    
    if (compId) {
      loadFailureModes(compId);
    } else {
      setFailureModes([]);
      setCurrentComponent(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!currentProject) {
      setError("No project selected. Please create or load a project first.");
      return;
    }

    if (!form.description.trim() || !form.failure_rate_total || !selectedComponent) {
      setError("Description, Failure Rate, and Component are required.");
      return;
    }

    const failureRate = parseFloat(form.failure_rate_total);
    if (isNaN(failureRate) || failureRate < 0) {
      setError("Failure Rate must be a valid positive number.");
      return;
    }

    if (!form.is_SPF && !form.is_MPF) {
      setError("At least one failure type (SPF or MPF) must be selected.");
      return;
    }

    // Check for duplicate description
    const existingFM = failureModes.find(fm => 
      fm.description.toLowerCase() === form.description.toLowerCase() && 
      fm.id !== editingId
    );
    if (existingFM) {
      setError(`Failure mode with description '${form.description}' already exists for this component.`);
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const failureModeData = {
        ...form,
        component: selectedComponent,
        Failure_rate_total: failureRate
      };

      console.log("Creating failure mode with data:", failureModeData);
      console.log("Form state:", form);
      console.log("Selected component:", selectedComponent);
      console.log("Failure rate:", failureRate);

      if (editingId) {
        await updateFailureMode(editingId, failureModeData);
      } else {
        await createFailureMode(failureModeData);
      }

      // Reset form
      setForm({
        description: "",
        failure_rate_total: "",
        system_level_effect: "",
        is_SPF: false,
        is_MPF: false,
        SPF_safety_mechanism: "",
        SPF_diagnostic_coverage: "",
        MPF_safety_mechanism: "",
        MPF_diagnostic_coverage: "",
        component: selectedComponent
      });
      setEditingId(null);

      // Reload failure modes
      await loadFailureModes(selectedComponent);
    } catch (error) {
      console.error("Failed to save failure mode:", error);
      setError("Failed to save failure mode. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (failureMode) => {
    setForm({
      description: failureMode.description,
      failure_rate_total: failureMode.failure_rate_total.toString(),
      system_level_effect: failureMode.system_level_effect,
      is_SPF: failureMode.is_SPF,
      is_MPF: failureMode.is_MPF,
      SPF_safety_mechanism: failureMode.SPF_safety_mechanism,
      SPF_diagnostic_coverage: failureMode.SPF_diagnostic_coverage.toString(),
      MPF_safety_mechanism: failureMode.MPF_safety_mechanism,
      MPF_diagnostic_coverage: failureMode.MPF_diagnostic_coverage.toString(),
      component: failureMode.component
    });
    setEditingId(failureMode.id);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this failure mode?")) {
      return;
    }

    try {
      await deleteFailureMode(id);
      await loadFailureModes(selectedComponent);
    } catch (error) {
      console.error("Failed to delete failure mode:", error);
      setError("Failed to delete failure mode.");
    }
  };

  const handleContinue = () => {
    navigate("/fmeda-analysis");
  };

  if (!currentProject) {
    return (
      <div className={styles.container}>
        <div className={styles.backdrop}></div>
        <div className={styles.noProject}>
          <h2>⚠️ No Project Selected</h2>
          <p>Please create or load a project first to manage failure modes.</p>
          <button className={styles.backBtn} onClick={() => navigate("/")}>
            <span className={styles.btnIcon}>🏠</span>
            <span>Go to Home</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.backdrop}></div>
      
      <div className={styles.header}>
        <h2>🔧 Component Failure Modes</h2>
        <p className={styles.projectInfo}>
          Project: <span className={styles.projectName}>{currentProject.name}</span>
        </p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.formRow}>
          <div className={styles.formGroup}>
            <label className={styles.label}>
              <span className={styles.labelIcon}>🔧</span>
              Select Component
            </label>
            <select
              name="component"
              value={selectedComponent || ""}
              onChange={handleComponentChange}
              className={styles.select}
              required
            >
              <option value="">Select a component...</option>
              {components.map((comp) => (
                <option key={comp.id} value={comp.id}>
                  {comp.comp_id} - {comp.type}
                </option>
              ))}
            </select>
            {currentComponent && (
              <p className={styles.helpText}>
                Selected: {currentComponent.comp_id} ({currentComponent.type}) - 
                Failure Rate: {currentComponent.failure_rate} FIT
              </p>
            )}
          </div>
        </div>

        <div className={styles.formSection}>
          <div className={styles.sectionHeader}>
            <h3>✏️ Manual Failure Mode Entry</h3>
            <p>Add custom failure modes manually</p>
          </div>

          {selectedComponent && (
            <>
              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>
                    <span className={styles.labelIcon}>📝</span>
                    Failure Mode Description
                  </label>
                  <textarea
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                    placeholder="Describe the failure mode..."
                    className={styles.textarea}
                    rows="3"
                    required
                  />
                </div>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>
                    <span className={styles.labelIcon}>📊</span>
                    Failure Rate (FIT)
                  </label>
                  <input
                    name="failure_rate_total"
                    type="number"
                    step="0.01"
                    min="0"
                    value={form.failure_rate_total}
                    onChange={handleChange}
                    placeholder="e.g., 100, 250.5"
                    className={styles.input}
                    required
                  />
                </div>
                <div className={styles.formGroup}>
                  <label className={styles.label}>
                    <span className={styles.labelIcon}>⚡</span>
                    System Level Effect
                  </label>
                  <input
                    name="system_level_effect"
                    type="text"
                    value={form.system_level_effect}
                    onChange={handleChange}
                    placeholder="e.g., Loss of function, Degraded performance"
                    className={styles.input}
                  />
                </div>
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.checkboxLabel}>
                    <input
                      name="is_SPF"
                      type="checkbox"
                      checked={form.is_SPF}
                      onChange={handleChange}
                      className={styles.checkbox}
                    />
                    <span className={styles.checkboxText}>
                      <span className={styles.checkboxIcon}>🚨</span>
                      Single Point Failure (SPF)
                    </span>
                  </label>
                </div>
                <div className={styles.formGroup}>
                  <label className={styles.checkboxLabel}>
                    <input
                      name="is_MPF"
                      type="checkbox"
                      checked={form.is_MPF}
                      onChange={handleChange}
                      className={styles.checkbox}
                    />
                    <span className={styles.checkboxText}>
                      <span className={styles.checkboxIcon}>⚠️</span>
                      Multiple Point Failure (MPF)
                    </span>
                  </label>
                </div>
              </div>

              {form.is_SPF && (
                <div className={styles.formRow}>
                  <div className={styles.formGroup}>
                    <label className={styles.label}>
                      <span className={styles.labelIcon}>🛡️</span>
                      SPF Safety Mechanism
                    </label>
                    <input
                      name="SPF_safety_mechanism"
                      type="text"
                      value={form.SPF_safety_mechanism}
                      onChange={handleChange}
                      placeholder="Describe the SPF safety mechanism..."
                      className={styles.input}
                    />
                  </div>
                  <div className={styles.formGroup}>
                    <label className={styles.label}>
                      <span className={styles.labelIcon}>📈</span>
                      SPF Diagnostic Coverage (%)
                    </label>
                    <input
                      name="SPF_diagnostic_coverage"
                      type="number"
                      step="0.1"
                      min="0"
                      max="100"
                      value={form.SPF_diagnostic_coverage}
                      onChange={handleChange}
                      placeholder="0-100"
                      className={styles.input}
                    />
                  </div>
                </div>
              )}

              {form.is_MPF && (
                <div className={styles.formRow}>
                  <div className={styles.formGroup}>
                    <label className={styles.label}>
                      <span className={styles.labelIcon}>🛡️</span>
                      MPF Safety Mechanism
                    </label>
                    <input
                      name="MPF_safety_mechanism"
                      type="text"
                      value={form.MPF_safety_mechanism}
                      onChange={handleChange}
                      placeholder="Describe the MPF safety mechanism..."
                      className={styles.input}
                    />
                  </div>
                  <div className={styles.formGroup}>
                    <label className={styles.label}>
                      <span className={styles.labelIcon}>📈</span>
                      MPF Diagnostic Coverage (%)
                    </label>
                    <input
                      name="MPF_diagnostic_coverage"
                      type="number"
                      step="0.1"
                      min="0"
                      max="100"
                      value={form.MPF_diagnostic_coverage}
                      onChange={handleChange}
                      placeholder="0-100"
                      className={styles.input}
                    />
                  </div>
                </div>
              )}

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
                    {isLoading ? "Saving..." : (editingId ? "Update Failure Mode" : "Add Failure Mode")}
                  </span>
                </button>
                
                {editingId && (
                  <button
                    type="button"
                    className={styles.cancelBtn}
                    onClick={() => {
                      setForm({
                        description: "",
                        failure_rate_total: "",
                        system_level_effect: "",
                        is_SPF: false,
                        is_MPF: false,
                        SPF_safety_mechanism: "",
                        SPF_diagnostic_coverage: "",
                        MPF_safety_mechanism: "",
                        MPF_diagnostic_coverage: "",
                        component: selectedComponent
                      });
                      setEditingId(null);
                    }}
                  >
                    <span className={styles.btnIcon}>❌</span>
                    <span>Cancel</span>
                  </button>
                )}
              </div>
            </>
          )}
        </div>
      </form>

      {error && <div className={styles.error}>{error}</div>}

      {selectedComponent && (
        <div className={styles.tableSection}>
          <div className={styles.tableHeader}>
            <h3>Failure Modes for {currentComponent?.comp_id} ({failureModes.length})</h3>
            {failureModes.length > 0 && (
              <button 
                className={styles.continueBtn} 
                onClick={handleContinue}
              >
                <span className={styles.btnIcon}>🚀</span>
                <span>Continue to FMEDA Analysis</span>
                <span className={styles.btnArrow}>→</span>
              </button>
            )}
          </div>

          {failureModes.length === 0 ? (
            <div className={styles.emptyState}>
              <div className={styles.emptyIcon}>🔧</div>
              <h4>No Failure Modes Defined</h4>
              <p>Add failure modes for this component above to continue with your FMEDA analysis.</p>
              <p>Failure modes describe how components can fail and their safety mechanisms.</p>
            </div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Description</th>
                  <th>FIT Rate</th>
                  <th>System Effect</th>
                  <th>SPF</th>
                  <th>SPF Mechanism</th>
                  <th>SPF DC%</th>
                  <th>MPF</th>
                  <th>MPF Mechanism</th>
                  <th>MPF DC%</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {failureModes.map((fm) => (
                  <tr key={fm.id}>
                    <td className={styles.description}>{fm.description}</td>
                    <td className={styles.failureRate}>{fm.failure_rate_total}</td>
                    <td className={styles.systemEffect}>{fm.system_level_effect}</td>
                    <td className={styles.spf}>
                      {fm.is_SPF ? "✅ Yes" : "❌ No"}
                    </td>
                    <td className={styles.spfMechanism}>{fm.SPF_safety_mechanism || "-"}</td>
                    <td className={styles.spfDc}>
                      {fm.is_SPF ? `${fm.SPF_diagnostic_coverage}%` : "N/A"}
                    </td>
                    <td className={styles.mpf}>
                      {fm.is_MPF ? "✅ Yes" : "❌ No"}
                    </td>
                    <td className={styles.mpfMechanism}>{fm.MPF_safety_mechanism || "-"}</td>
                    <td className={styles.mpfDc}>
                      {fm.is_MPF ? `${fm.MPF_diagnostic_coverage}%` : "N/A"}
                    </td>
                    <td className={styles.actions}>
                      <button 
                        className={styles.editBtn} 
                        onClick={() => handleEdit(fm)}
                        title="Edit Failure Mode"
                      >
                        <span className={styles.btnIcon}>✏️</span>
                        <span>Edit</span>
                      </button>
                      <button 
                        className={styles.deleteBtn} 
                        onClick={() => handleDelete(fm.id)}
                        title="Delete Failure Mode"
                      >
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
      )}
    </div>
  );
} 