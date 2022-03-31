import React, { useState, useEffect } from 'react'
import { Form, Button, Row, Col } from 'react-bootstrap'
import axios from 'axios';
import Select from 'react-select';

// Contains forms for searching for a course
// The function for handling the submit button (handler) is passed in as a prop
const SearchForm = ({ handler }) => {

    const [school, setSchool] = useState('guelph');
    let courseObj = JSON.parse(localStorage.getItem('courseName'));

    const [depts, setDepts] = useState();

    const fetchDepts = async (param) => {
        axios.get(global.config.base_url + '/get_departments_list', { params: param }).then((res) => {

            // no courses were found
            if (res.data.length === 0) {
                // Reset courses to initial state, so it shows no courses found
                setDepts(null);
                return;
            }

            setDepts(res.data);

        }, (err) => { // an error occured
            console.log(err);
        });
    }

    useEffect(() => {  
        
        fetchDepts({"school": school});

    }, [])
    

    return (
        <div className='courseSearch'>
            <Form onSubmit={handler} bg="dark" expand="lg" letiant="dark">

                <Form.Group as={Col} className="mb-3">
                        <Form.Label>Select School</Form.Label>
                        <Form.Select 
                            defaultValue='guelph' 
                            id="courseSearchSchoolId"
                            onChange={(e) => {
                                setSchool(e.target.value);
                                fetchDepts({ "school": e.target.value })
                            }}
                            >
                            <option value='guelph'>Guelph University</option>
                            <option value='carleton'>Carleton University</option>
                        </Form.Select>
                </Form.Group>

                <Row>
                    <Form.Group as={Col} className="mb-3">
                        <Form.Label>Course Name</Form.Label>
                        <Form.Control type='name' defaultValue={courseObj === null ? "" : courseObj['name']} placeholder='Course Name' id="courseName" />
                    </Form.Group>
                </Row>

                <Row>
                    
                    <Form.Group as={Col} className="mb-3">
                        <Form.Label>Select Department</Form.Label>
                        <Select options={depts}/>
                    </Form.Group>

                    <Form.Group as={Col} className="mb-3">
                        <Form.Label>Course Code</Form.Label>
                        <Form.Control type='code' placeholder='Course Code/Number' id="courseCode" />
                    </Form.Group>

                    <Form.Group as={Col} className="mb-3">
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

                {school === 'guelph' ?
                    <Row>
                        <Form.Group className='mb-3'>
                            <Form.Check type='checkbox' label='F' inline='true' id="fallCheckbox" />
                            <Form.Check type='checkbox' label='W' inline='true' id="winterCheckbox" />
                            <Form.Check type='checkbox' label='S' inline='true' id="summerCheckbox" />
                        </Form.Group>
                    </Row>
                : null}

                <Button type='submit'>Search</Button>

                
            </Form>
        </div>
    )
}

export default SearchForm
