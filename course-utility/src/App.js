import './App.css';
import Navbar from './components/global/Navbar'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import { useState } from "react";

import CourseSearch from './pages/CourseSearch';
import MakeGraph from './pages/MakeGraph';
import NoPage from './pages/NoPage';
import Home from './pages/Home';


function App() {

  const [links] = useState([

    {
      text: 'home',
      linkTo: '/'
    },
    {
      text: 'Make Graph',
      linkTo: '/makegraph'
    },
    {
      text: 'Course Search',
      linkTo: '/coursesearch'
    }
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

        </Routes>

      </Router>
    </div>
  );
}

export default App;
