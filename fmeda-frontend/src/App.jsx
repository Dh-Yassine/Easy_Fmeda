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

export default function App() {
  const [currentProject, setCurrentProject] = useState(null);

  // Function to clear all project data
  const clearProjectData = () => {
    setCurrentProject(null);
    localStorage.removeItem('currentProject');
    sessionStorage.clear();
  };

  return (
    <Router>
      <div className="App">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route 
              path="/" 
              element={
                <Home 
                  currentProject={currentProject} 
                  setCurrentProject={setCurrentProject}
                  clearProjectData={clearProjectData}
                />
              } 
            />
            <Route 
              path="/assumptions" 
              element={
                <Assumptions 
                  currentProject={currentProject} 
                  setCurrentProject={setCurrentProject} 
                />
              } 
            />
            <Route 
              path="/safety-functions" 
              element={
                <SafetyFunctions 
                  currentProject={currentProject} 
                  setCurrentProject={setCurrentProject} 
                />
              } 
            />
            <Route 
              path="/components" 
              element={
                <Components 
                  currentProject={currentProject} 
                  setCurrentProject={setCurrentProject} 
                />
              } 
            />
            <Route 
              path="/failure-modes" 
              element={
                <FailureModes 
                  currentProject={currentProject} 
                  setCurrentProject={setCurrentProject} 
                />
              } 
            />
            <Route 
              path="/failure-modes/:componentId" 
              element={
                <FailureModes 
                  currentProject={currentProject} 
                  setCurrentProject={setCurrentProject} 
                />
              } 
            />
            <Route 
              path="/fmeda-analysis" 
              element={
                <FMEDAAnalysis 
                  currentProject={currentProject} 
                  setCurrentProject={setCurrentProject} 
                />
              } 
            />
            <Route 
              path="/results" 
              element={
                <Results 
                  currentProject={currentProject} 
                  setCurrentProject={setCurrentProject} 
                />
              } 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
