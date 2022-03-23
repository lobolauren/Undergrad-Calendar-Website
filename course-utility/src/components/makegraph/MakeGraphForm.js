import React from "react";
import { useEffect, useState } from 'react';
import { Form, Button, Row, Col } from "react-bootstrap";

const MakeGraphForm = ({ handler }) => {

  const [selectOption, setSelectOption] = useState('course');

  const toTitleCase = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  return (
    <div className="graph-form">
        <Form onSubmit={handler} bg="dark" expand="lg" letiant="dark">
        <Form.Group className="mb-3">
          <Form.Label>Graph Type</Form.Label>
          <Form.Select 
            id="graphType"
            defaultValue="course" 
            onChange={(e) => setSelectOption(e.target.value)}
          >
            <option value="course">Course</option>
            <option value="department">Department</option>
            <option value="program">Program</option>
          </Form.Select>
        </Form.Group>

        {selectOption != 'catalog'
        ? <Form.Group className="mb-3">
            <Form.Label>{toTitleCase(selectOption)} Code</Form.Label>
            <Form.Control type="text" id="courseCode" required />
          </Form.Group>
        : null}

        {selectOption == 'program' 
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
