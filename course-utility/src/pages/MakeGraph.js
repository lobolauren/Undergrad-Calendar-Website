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
    let checkHold
    
    if (graphType == "program"){
      minorValue = event.target.minorId.checked;
      graphWanted = {
        "type": graphType,
        "code": courseCode,
        "minor":minorValue
      }
    }else{
      graphWanted = {
        "type": graphType,
        "code": courseCode
      }
    }

    if (graphWanted["type"] == "course" || graphWanted["type"] == "department"){
      //make call to check if page exists
      let courseSearchQuery = {
        "name": "",
        "code": courseCode,
        "weight": "all",
        "terms": "F,W,S" // convert to string because array causes issues with axios params
      }
      
      axios.get(global.config.base_url + '/courses', { params: courseSearchQuery }).then((res) => {
        checkHold = Object.keys(res.data).length;

        // navigates to a separate page to display the desired graph
        if (graphWanted["type"] == "course"){
          if(checkHold == 1){
            navigate('/graph/' + graphWanted["type"] + '/' + graphWanted["code"]);
          }
          else{
            alert("Invalid input. Could not graph.");
          }
        }else if (graphWanted["type"] == "department"){
          if(checkHold > 1){
            navigate('/graph/' + graphWanted["type"] + '/' + graphWanted["code"]);
          }
          else{
            alert("Invalid input. Could not graph.");
          }
        }

      }, (err) => { // an error occured
        console.log(err);
      });
    }else if(graphWanted["type"] == "program"){

      if(graphWanted["minor"]==true){
        navigate('/graph/' + graphWanted["type"] + '/' + "minor" + '/' + graphWanted["code"]);
      }else if(graphWanted["minor"]==false){
        navigate('/graph/' + graphWanted["type"] + '/' + graphWanted["code"]);
      }

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
