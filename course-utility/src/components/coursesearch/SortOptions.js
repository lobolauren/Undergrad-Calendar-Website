import React from 'react'
import { Form, Dropdown, Row, Col } from 'react-bootstrap'

const SortOptions = ({sortTypeHandler, sortOrderHandler}) => {

    return (
        <div className="container">
            <div className='sortOptions mt-5 row'>
                <Row>
                    <div className="align-items-center col-2">
                        <p className="col-2">Sort by</p>
                    </div>

                    <Form.Select id="typeOption" className="col-6" onChange={sortTypeHandler}>
                        <option value="courseCodeOption">Course Code</option>
                        <option value="courseNameOption">Course Name</option>
                    </Form.Select>

                    <Form.Select id="sortOrder" className="col-6" onChange={sortOrderHandler}>
                        <option value="ascending">Ascending</option>
                        <option value="descending">Descending</option>
                    </Form.Select>
                </Row>
            </div>
        </div>
    )
}

export default SortOptions