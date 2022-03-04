import React from 'react'
import { Form, Button, Row, Col } from 'react-bootstrap'

const SearchForm = () => {
    return (
        <div className='courseSearch'>
            <Form bg="dark" expand="lg" variant="dark">
                
                <Row>
                    <Form.Group as={Col}>
                        <Form.Label>Course Name</Form.Label>
                        <Form.Control type='name' placeholder='Course Name' />
                    </Form.Group>
                </Row>
                    
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label>Course Code</Form.Label>
                            <Form.Control type='code' placeholder='Course Code/Number'/>
                        </Form.Group>    
    
                        <Form.Group as={Col}>
                            <Form.Label>Select Weights</Form.Label>
                            <Form.Select defaultValue='all'>
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
                            <Form.Check type='checkbox' label='F' inline='true'/>
                            <Form.Check type='checkbox' label='W' inline='true'/>
                            <Form.Check type='checkbox' label='S' inline='true'/>
                        </div>
                    </Row>
                    
                <Button type='submit'>Search</Button>
            </Form>
        </div>
    )
}

export default SearchForm