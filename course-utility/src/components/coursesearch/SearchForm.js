import React from 'react'
import { Form, Button, Row, Col } from 'react-bootstrap'


class SearchForm extends React.Component {


    handleSubmit = (event) => {
        event.preventDefault();

        let courseName = event.target.courseName.value;
        let courseCode = event.target.courseCode.value;
        let courseWeight = event.target.courseWeights.value;
        let isFallSelected = event.target.fallCheckbox.checked;
        let isWinterSelected = event.target.winterCheckbox.checked;
        let isSummerSelected = event.target.summerCheckbox.checked;
        
        // get terms selected
        let terms = this.buildTermsArray(isFallSelected, isWinterSelected, isSummerSelected);

        let courseSearchQuery = {
            "courseName": courseName,
            "courseCode": courseCode,
            "courseWeight": courseWeight,
            "terms": terms
        }

        console.log(courseSearchQuery);
    }

    buildTermsArray(isFallSelected, isWinterSelected, isSummerSelected) {
        let terms = [];
        if (isFallSelected)
            terms.push("F");
        if (isWinterSelected)
            terms.push("W");
        if (isSummerSelected)
            terms.push("S");
        return terms;
    }

    render() {
        return (
            <div className='courseSearch'>
                <Form onSubmit={this.handleSubmit} bg="dark" expand="lg" letiant="dark">
                    
                    <Row>
                        <Form.Group as={Col}>
                            <Form.Label>Course Name</Form.Label>
                            <Form.Control type='name' placeholder='Course Name' id="courseName"/>
                        </Form.Group>
                    </Row>
                        
                        <Row>
                            <Form.Group as={Col}>
                                <Form.Label>Course Code</Form.Label>
                                <Form.Control type='code' placeholder='Course Code/Number' id="courseCode"/>
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
                                <Form.Check type='checkbox' label='F' inline='true' id="fallCheckbox"/>
                                <Form.Check type='checkbox' label='W' inline='true' id="winterCheckbox"/>
                                <Form.Check type='checkbox' label='S' inline='true' id="summerCheckbox"/>
                            </div>
                        </Row>
                        
                    <Button type='submit'>Search</Button>
                </Form>
            </div>
        )
    }
}

export default SearchForm