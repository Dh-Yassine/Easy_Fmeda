import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar/Sidebar";
import Home from "./pages/Home/Home";
import Assumptions from "./pages/Assumptions/Assumptions";
import SafetyFunctions from "./pages/SafetyFunctions/SafetyFunctions";
import Components from "./pages/Components/Components";
import FailureModes from "./pages/FailureModes/FailureModes";
import FMEDAAnalysis from "./pages/FMEDAAnalysis/FMEDAAnalysis";
import Results from "./pages/Results/Results";
import "./App.css";
import { Toaster } from "react-hot-toast";
import { AnimatePresence, motion } from "framer-motion";
import { useLocation } from "react-router-dom";

export function showToast(message, type = "success") {
  // Lazy import to avoid circular deps
  import("react-hot-toast").then(({ toast }) => {
    if (type === "error") toast.error(message);
    else if (type === "loading") toast.loading(message);
    else toast.success(message);
  });
}

export default function App() {
  const [currentProject, setCurrentProject] = useState(null);
  const location = useLocation();

  // Function to clear all project data
  const clearProjectData = () => {
    setCurrentProject(null);
    localStorage.removeItem('currentProject');
    sessionStorage.clear();
  };

  return (
    <div className="App">
      <Sidebar />
      <main className="main-content">
        <Toaster position="top-right" toastOptions={{ duration: 3500 }} />
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            {/* For each route, wrap the element in a motion.div for animation */}
            <Route path="/" element={
              <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }} transition={{ duration: 0.35 }}>
                <Home currentProject={currentProject} setCurrentProject={setCurrentProject} clearProjectData={clearProjectData} />
              </motion.div>
            } />
            <Route path="/assumptions" element={
              <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }} transition={{ duration: 0.35 }}>
                <Assumptions currentProject={currentProject} setCurrentProject={setCurrentProject} />
              </motion.div>
            } />
            <Route path="/safety-functions" element={
              <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }} transition={{ duration: 0.35 }}>
                <SafetyFunctions currentProject={currentProject} setCurrentProject={setCurrentProject} />
              </motion.div>
            } />
            <Route path="/components" element={
              <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }} transition={{ duration: 0.35 }}>
                <Components currentProject={currentProject} setCurrentProject={setCurrentProject} />
              </motion.div>
            } />
            <Route path="/failure-modes" element={
              <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }} transition={{ duration: 0.35 }}>
                <FailureModes currentProject={currentProject} setCurrentProject={setCurrentProject} />
              </motion.div>
            } />
            <Route path="/failure-modes/:componentId" element={
              <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }} transition={{ duration: 0.35 }}>
                <FailureModes currentProject={currentProject} setCurrentProject={setCurrentProject} />
              </motion.div>
            } />
            <Route path="/fmeda-analysis" element={
              <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }} transition={{ duration: 0.35 }}>
                <FMEDAAnalysis currentProject={currentProject} setCurrentProject={setCurrentProject} />
              </motion.div>
            } />
            <Route path="/results" element={
              <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -24 }} transition={{ duration: 0.35 }}>
                <Results currentProject={currentProject} setCurrentProject={setCurrentProject} />
              </motion.div>
            } />
          </Routes>
        </AnimatePresence>
      </main>
    </div>
  );
}
