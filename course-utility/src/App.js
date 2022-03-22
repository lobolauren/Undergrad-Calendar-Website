import { useState } from "react";
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import React, { useEffect } from 'react'
import ReactDOM from 'react-dom'
import Navbar from './components/global/Navbar'
import CourseSearch from './pages/CourseSearch';
import MakeGraph from './pages/MakeGraph';
import NoPage from './pages/NoPage';
import Graph from './pages/Graph';
import Home from './pages/Home';

import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  useEffect(() => {
    document.title = "Course Utility"
  }, [])
  const [links] = useState([
    {text: 'Home', linkTo: '/'},
    {text: 'Make Graph', linkTo: '/makegraph'},
    {text: 'Course Search', linkTo: '/coursesearch'}
  ])

  return (
    <div className="App">
      <Navbar links={links} />
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/*" element={<NoPage />} />
          <Route path="/makegraph" element={<MakeGraph />} />
          <Route path="/coursesearch" element={<CourseSearch />} />
          <Route path="/graph/:type/:code" element={<Graph />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
