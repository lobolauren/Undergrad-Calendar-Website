import React from 'react'
import logo from '../assets/uogLogo.png'
import { useNavigate } from 'react-router-dom';

import { useState } from "react";

import { Container } from 'react-bootstrap'
import HomeSearch from '../components/home/HomeSearch'

const Home = () => {

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

    // hook containing courses
    const [courses, setCourses] = useState();
    
    return (
        <Container className="mt-5">
            <div class="home">
                <img src={logo} alt="logo" className="img-fluid" />
            </div>
            <div class="home">
                <h1>Welcome to University of Guelph Course Utility!</h1>
            </div>
            <HomeSearch handler={handleSubmit}/>
        </Container>
    )
}

export default Home
