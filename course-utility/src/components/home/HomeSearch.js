import React from 'react'
import { Form, Button, Row, Col } from 'react-bootstrap'

// Simple course search by name to redirect the user to the coursesearch page for more indepth course searches
// The function for handling the submit button (handler) is passed in as a prop
const HomeSearch = ({ handler }) => {
    return (
        <div className='home-search'>
            <Form onSubmit={handler} bg="dark" expand="lg" letiant="dark">
  
                <Row>
                    <Form.Group as={Col} className="mb-3">
                        <Form.Label><h5>Search course:</h5></Form.Label>
                        <Form.Control type='name' placeholder='Course Name' id="courseName" />
                    </Form.Group>
                </Row>
  
                <Button type='submit'>Search</Button>
  
                
            </Form>
        </div>
    )
  }
  
  export default HomeSearch