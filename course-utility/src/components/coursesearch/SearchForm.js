import React from 'react'
import { Form, Button, Row, Col } from 'react-bootstrap'

// Contains forms for searching for a course
// The function for handling the submit button (handler) is passed in as a prop
const SearchForm = ({ handler }) => {
  return (
      <div className='courseSearch'>
          <Form onSubmit={handler} bg="dark" expand="lg" letiant="dark">

              <Row>
                  <Form.Group as={Col}>
                      <Form.Label>Course Name</Form.Label>
                      <Form.Control type='name' placeholder='Course Name' id="courseName" />
                  </Form.Group>
              </Row>

              <Row>
                  <Form.Group as={Col}>
                      <Form.Label>Course Code</Form.Label>
                      <Form.Control type='code' placeholder='Course Code/Number' id="courseCode" />
                  </Form.Group>

                  <Form.Group as={Col}>
                      <Form.Label>Select Weights</Form.Label>
                      <Form.Select defaultValue='all' id="courseWeights">
                          <option>all</option>
                          <option>0.25</option>
                          <option>0.5</option>
                          <option>0.75</option>
                          <option>1.0</option>
                      </Form.Select>
                  </Form.Group>

              </Row>

              <Row>
                  <div className='termBox'>
                      <Form.Check type='checkbox' label='F' inline='true' id="fallCheckbox" />
                      <Form.Check type='checkbox' label='W' inline='true' id="winterCheckbox" />
                      <Form.Check type='checkbox' label='S' inline='true' id="summerCheckbox" />
                  </div>
              </Row>

              <Button type='submit'>Search</Button>
          </Form>
      </div>
  )
}

export default SearchForm