import React from 'react'
import { Form, Row } from 'react-bootstrap'

const SortOptions = ({sortTypeHandler, sortOrderHandler}) => {

    return (
        <Row className="mt-3">
            <div className="align-self-center">
                <p>Sort by</p>
            </div>

            <div className="col-2">
                <Form.Select id="typeOption" onChange={sortTypeHandler}>
                    <option value="courseCodeOption">Course Code</option>
                    <option value="courseNameOption">Course Name</option>
                </Form.Select>
            </div>

            <div className="col-2">
                <Form.Select id="sortOrder" onChange={sortOrderHandler}>
                    <option value="ascending">Ascending</option>
                    <option value="descending">Descending</option>
                </Form.Select>
            </div>
        </Row>
    )
}

export default SortOptions