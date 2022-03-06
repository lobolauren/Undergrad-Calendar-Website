import React from 'react'
import { Container } from 'react-bootstrap'
import InfoModal from '../components/makegraph/InfoModal'
import MakegraphOption from '../components/makegraph/makegraphOption'
import { Form, Button, Row, Col } from 'react-bootstrap'

const MakeGraph = () => {
    
  return (
    <Container className="mt-40">
      <span>
        <h1>Make Graph <InfoModal /></h1>
        <br/><br/><br/>
        <h2>Desired Graph Style: </h2>
       
        <MakegraphOption/>
      </span>
    </Container>
    
  )
}

export default MakeGraph
