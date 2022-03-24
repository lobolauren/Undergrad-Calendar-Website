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

    let minorValue=false;
    let graphType = event.target.graphType.value;
    let courseCode = event.target.courseCode.value;
    let graphWanted = {}
    let schoolChoice = event.target.schoolChoice.value;
    console.log("School choosen is " + schoolChoice);
    
    if (graphType == "program"){
      minorValue = event.target.minorId.checked;
      graphWanted = {
        "school": schoolChoice,
        "type": graphType,
        "code": courseCode,
        "minor":minorValue
      }
    }else{
      graphWanted = {
        "school": schoolChoice,
        "type": graphType,
        "code": courseCode
      }
    }

    // navigates to a separate page to display the desired graph
    if (graphWanted["type"] == "course" || graphWanted["type"] == "department"){
      navigate('/graph/' + graphWanted["type"] + '/' + graphWanted["code"]);
    }else if (graphWanted["type"] == "program" && graphWanted["minor"]==true){
      navigate('/graph/' + graphWanted["type"] + '/' + "minor" + '/' + graphWanted["code"]);
    }else if (graphWanted["type"]=="catalog" || (graphWanted["type"] == "program" && graphWanted["minor"]==false)){
      navigate('/graph/' + graphWanted["type"] + '/' + graphWanted["code"]);
    }
  }
    
  return (
    <Container className="mt-5">
      <h2>Make Graph <InfoModal/></h2>      
      <MakeGraphForm handler={handleSubmit}/>
    </Container>
  )
}

export default MakeGraph
