import React from 'react'
import logo from './uogLogo.png'
import axios from 'axios';

import { useEffect, useState } from "react";
import { Button } from 'react-bootstrap'

const Home = () => {

    const [data, setData] = useState([]);

    useEffect( () => {

        const fetchData = async () => {
          axios.get(global.config.base_url + '/').then((res) => {
            setData(res.data);
          });
        }
        fetchData();
    }, []);

    console.log(data);
    
    function buttonClick() {
        alert(data)
    }

    return (
        <div className="pageContainer text-center">
            <img src={logo} alt="logo" className="img-fluid" />

            <h1>Welcome to University of Guelph Course Utility!</h1>
	    
            <Button as="input" type="button" variant="success" value="API Call" onClick={buttonClick}/>

        </div>
    )
}

export default Home
