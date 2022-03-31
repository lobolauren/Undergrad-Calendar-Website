import React from 'react'
import { Form, Col } from 'react-bootstrap'

const DepartmentSelect = ({ depts }) => {
    console.log(depts);
  return (
      <Form.Group as={Col} className="mb-3">
          <Form.Label>Select Department</Form.Label>
          <Form.Select defaultValue='' id="departmentSelect">
              <option></option>
              { depts ?
                  React.Children.toArray(
                      depts.map((dept) => {
                          <option>{dept}</option>
                      })
                  )
              : <></>}
          </Form.Select>
      </Form.Group>
  )
}

export default DepartmentSelect