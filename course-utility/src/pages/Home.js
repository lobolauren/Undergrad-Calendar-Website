import React from 'react'
import logo from '../assets/uogLogo.png'
import axios from 'axios';

import { useEffect, useState } from "react";
import { Button } from 'react-bootstrap'

const Home = () => {
    
    return (
        <div className="pageContainer text-center">
            <img src={logo} alt="logo" className="img-fluid" />

            <h1>Welcome to University of Guelph Course Utility!</h1>

        </div>
    )
}

export default Home
