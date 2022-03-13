import React from 'react'
import logo from './uogLogo.png'
import { useEffect, useState } from "react";
import axios from 'axios';

const Home = () => {

    const [data, setData] = useState([]);

    useEffect( () => {

        const fetchData = async () => {
          axios.get("https://131.104.49.102/api/").then( (res) => {
            setData(res.data);
          });

        }

        fetchData();

    },[]);

    console.log(data);
    
    function buttonClick() {
	alert(data);
    }

    return (
        <div className="pageContainer text-center">
            <img src={logo} alt="logo" className="img-fluid" />

            <h1>Welcome to University of Guelph Course Utility! {data}</h1>
	    
	    <button onClick={buttonClick}>API CALL</button>

        </div>
    )
}

export default Home
