import React from 'react'
import uogLogo from '../assets/uogLogoAlt.png'
import carletonLogo from '../assets/carletonLogo.png'
import { useNavigate } from 'react-router-dom';

import { Container } from 'react-bootstrap'
import HomeSearch from '../components/home/HomeSearch'

const Home = () => {

    // Clear potential course name from home search
    localStorage.clear();

    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();

        let courseName = event.target.courseName.value;
        let courseSearchQuery = {
            "name": courseName
        }
        localStorage.setItem('courseName', JSON.stringify(courseSearchQuery))

        navigate('/coursesearch')
    }
    
    return (
        <Container className="mt-5">
            <div className="home-img">
                <img src={uogLogo} alt="logo" className="uog" />
                <img src={carletonLogo} alt="logo" className="carleton" />
            </div>
            <div className="home">
                <h1>Course Utility</h1>
            </div>
            <HomeSearch handler={handleSubmit}/>
        </Container>
    )
}

export default Home
