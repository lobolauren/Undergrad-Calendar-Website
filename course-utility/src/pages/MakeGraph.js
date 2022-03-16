import React, { useState, useEffect } from 'react'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import { Container } from 'react-bootstrap'
import InfoModal from '../components/makegraph/InfoModal'
import MakeGraphForm from '../components/makegraph/MakeGraphForm'
import { Form, Button, Row, Col } from 'react-bootstrap'

const MakeGraph=()=>{

  const navigate = useNavigate();
  
  const handleSubmit = (event) => {
    event.preventDefault();

    let graphType = event.target.graphType.value;
    let courseCode = event.target.courseCode.value;

    let graphWanted = {
        "type": graphType,
        "code": courseCode
    }

    navigate('/graph/' + graphWanted["type"] + '/' + graphWanted["code"]);
  }
    
  return (
    <Container className="mt-5">
      <h2>Make Graph <InfoModal/></h2>      
      <MakeGraphForm handler={handleSubmit}/>
    </Container>
  )
}

export default MakeGraph
