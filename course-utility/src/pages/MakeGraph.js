import React from 'react'
import { Container } from 'react-bootstrap'
import InfoModal from '../components/makegraph/InfoModal'
import MakeGraphForm from '../components/makegraph/MakeGraphForm'
import { Form, Button, Row, Col } from 'react-bootstrap'

const MakeGraph=()=>{
    
  return (
    <Container className="mt-5">
      <h2>Make Graph <InfoModal/></h2>
      <MakeGraphForm/>
    </Container>
  )
}

export default MakeGraph
