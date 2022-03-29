import React from 'react'
import sad_face from '../assets/404-sadface.png'
import { Container } from 'react-bootstrap'
import { useNavigate } from "react-router-dom";
import { Form, Button, Row, Col } from 'react-bootstrap'

const NoPage = () => {
    let navigate = useNavigate();
    const goHome = () =>{
        let path = "/";
        navigate(path);
    }

    return (
        <Container className="mt-5">
            <div className='home'><h1>No Page Found: 404</h1></div>
            <div><br></br><br></br><br></br></div>
            <div className="home"><img src={sad_face} alt="sad_face" className="img-fluid" /></div>
            <div><br></br><br></br><br></br></div>
            <div className='home'><p>The page you were looking for does not exist.</p></div>
            <div><br></br><br></br></div>
            <div className='home' onClick={goHome}><Button type="submit">Return Home</Button></div>
        </Container>
    )
}

export default NoPage