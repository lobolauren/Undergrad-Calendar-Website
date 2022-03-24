import React from "react";
import { useState } from 'react';
import { Form, Button, Col } from "react-bootstrap";

const MakeGraphForm = ({ handler }) => {

  const [selectOption, setSelectOption] = useState('course');
  const [selectOptionSchool, setSelectSchool] = useState('Guelph University');

  const toTitleCase = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  return (
    <div className="graph-form">
        <Form onSubmit={handler} bg="dark" expand="lg" letiant="dark">
        <Form.Group className="mb-3">

          <Form.Group as={Col} className="mb-3">
            <Form.Label>Select School</Form.Label>
            <Form.Select 
              defaultValue='guelph' 
              id="courseSearchSchoolId"
              onChange={(e) => setSelectSchool(e.target.value)}
            >
              <option>Guelph University</option>
              <option>Carleton University</option>
            </Form.Select>
          </Form.Group>

          <Form.Label>Graph Type</Form.Label>
          <Form.Select 
            id="graphType"
            defaultValue="course" 
            onChange={(e) => setSelectOption(e.target.value)}
          >
            <option value="course">Course</option>
            <option value="department">Department</option>
            {selectOptionSchool === 'Guelph University' ?
            <option value="program">Program</option>
            : null}
          </Form.Select>
        </Form.Group>

        {selectOption !== 'catalog'
        ? <Form.Group className="mb-3">
            <Form.Label>{toTitleCase(selectOption)} Code</Form.Label>
            <Form.Control type="text" id="courseCode" required />
          </Form.Group>
        : null}

        {selectOption === 'program' && selectOptionSchool === 'Guelph University'
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
