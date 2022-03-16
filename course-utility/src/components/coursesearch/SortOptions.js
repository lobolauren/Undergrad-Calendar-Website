import React from 'react'
import { Dropdown } from 'react-bootstrap'

const SortOptions = () => {
    function updateDropdown(event) {
        console.log(event);
        if (event == "courseCodeOption") {
            // Course Code

        }
        else {
            // Set to Course Name
        }
    }

    return (
        <div className='sortOptions'>
            <p>Sort by</p>

            <Dropdown onSelect={updateDropdown}>
            <Dropdown.Toggle id="sortByOptions">
                Course Code
            </Dropdown.Toggle>

            <Dropdown.Menu>
                <Dropdown.Item eventKey="courseCodeOption">Course Code</Dropdown.Item>
                <Dropdown.Item eventKey="courseNameOption">Course Name</Dropdown.Item>
            </Dropdown.Menu>
            </Dropdown>
            
        </div>
    )
}

export default SortOptions