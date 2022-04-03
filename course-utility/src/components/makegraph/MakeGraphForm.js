import React from "react";
import { useState, useEffect } from 'react';
import { Form, Button, Col, Row } from "react-bootstrap";
import axios from 'axios';
import Select from 'react-select';

const MakeGraphForm = ({ handler, setSelectedDept }) => {

  const [selectOption, setSelectOption] = useState('course');
  const [selectOptionSchool, setSelectSchool] = useState('guelph');

  // department list with default value
  const [depts, setDepts] = useState([
    { label: 'all', value: '' }
  ]);

  // get a list of departmemts
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

  // get a list of programs & sets the depts hook to it (for simplicity)
  const fetchPrograms = async (param) => {
    axios.get(global.config.base_url + '/get_programs_list').then((res) => {

      // no courses were found
      if (res.data.length === 0) {
        // Reset courses to initial state, so it shows no courses found
        setDepts(null);
        return;
      }

      let programsSet = [];
      res.data.programs.forEach(element => {
        programsSet.push({ label: element.toUpperCase(), value: element.toUpperCase()});
      });

      setDepts(programsSet);

    }, (err) => { // an error occured
      console.log(err);
    });
  }

  useEffect(() => {

    fetchDepts({ "school": selectOptionSchool });

  }, [])

  return (
    <div className="graph-form">
        <Form onSubmit={handler} bg="dark" expand="lg" letiant="dark">
        <Form.Group className="mb-3">

          <Form.Group as={Col} className="mb-3">
            <Form.Label>Select School</Form.Label>
            <Form.Select 
              defaultValue='Guelph University' 
              id="courseSearchSchoolId"
              onChange={(e) => {
                setSelectSchool(e.target.value)
                fetchDepts({school: e.target.value});
              }}
            >
              <option value={'guelph'}>Guelph University</option>
              <option value={'carleton'}>Carleton University</option>
            </Form.Select>
          </Form.Group>

          <Form.Label>Graph Type</Form.Label>
          <Form.Select 
            id="graphType"
            defaultValue="course" 
            onChange={(e) => {
              setSelectOption(e.target.value);
              if(e.target.value === 'program'){
                fetchPrograms();
              } else {
                fetchDepts({school: selectOptionSchool});
              }
            }}
            className="mb-3"
          >
            <option value="course">Course</option>
            <option value="department">Department</option>
            {selectOptionSchool === 'guelph' ?
            <option value="program">Program</option>
            : null}
          </Form.Select>
        </Form.Group>

        <Row>

          <Form.Group as={Col} className="mb-3">
            <Form.Label>Select {selectOption === 'program' ? 'Program' : 'Department'}</Form.Label>
            <Select required options={depts} onChange={(e) => {
              setSelectedDept(e.value);
            }} />
          </Form.Group>

          {selectOption === 'course' ?
            <Form.Group as={Col} className="mb-3">
              <Form.Label>Course Code</Form.Label>
              <Form.Control type="text" placeholder='Enter Digits Only (ex. 1300)' id="courseCode" required onKeyPress={(e) => {
                const re = /[0-9]/;
                if (!re.test(e.key)) {
                  e.preventDefault();
                }
              }}/>
            </Form.Group>
          : null}

        </Row>

        {selectOption === 'program' && selectOptionSchool === 'guelph'
        ? <Form.Group className="mb-3">
            <Form.Label>Major or Minor</Form.Label>
            <Form.Check type="radio" name="major-minor" label="Major" value="major" required />
            <Form.Check type="radio" name="major-minor" label="Minor" value="minor" id="minorId"/>
          </Form.Group>
        : null}

        <Button type='submit'>View Graph</Button>
      </Form>
    </div>
  );
};

export default MakeGraphForm;
