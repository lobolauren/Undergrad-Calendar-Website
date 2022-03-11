import React from 'react'
import logo from './uogLogo.png'
import { useEffect, useState } from "react";
import axios from 'axios';

const Home = () => {

    const [data, setData] = useState([]);

    useEffect( () => {

        const fetchData = async () => {
          axios.get("http://localhost:5000/").then( (res) => {
            setData(res.data);
          });

        }

        fetchData();

    },[]);
    console.log(data);
    return (
        <div className="pageContainer text-center">
            <img src={logo} alt="logo" className="img-fluid" />

            <h1>Welcome to University of Guelph Course Utility! {data}</h1>

        </div>
    )
}

export default Home
