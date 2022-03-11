import React from 'react';
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import { solid, regular, brands } from '@fortawesome/fontawesome-svg-core/import.macro'
import { Form, Button, Row, Col } from 'react-bootstrap';
import ReactTooltip from "react-tooltip";

const MakegraphOption=()=>{
    return (
        
            <Form bg="dark" expand="lg" variant="dark">
                
                <Row>
                    <div className='termBox'>
                    <link rel="stylesheet" type="text/css" href="bootstrap/dist/css/bootstrap.min.css" />
                    <link rel="stylesheet" type="text/css" href="https://netdna.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" />
                    <link rel="stylesheet" type="text/css" href="https://flatlogic.github.io/awesome-bootstrap-checkbox/demo/build.css" />
                        <div class="form-check">
                            <input id="departmentInput" type="radio" name="flexRadioDefault" data-for="departmentTip" class="form-check-input"/>
                            <label for="departmentInput" data-tip data-for="departmentTip">
                                Department Graph
                            </label>

                            <ReactTooltip id="departmentTip" place="right" effect="solid">
                                Graphes the desired deparment (Ex: CIS)
                            </ReactTooltip>
                        </div>
                        <div class="form-check">
                            <input id="programInput" type="radio" name="flexRadioDefault" data-for="programTip" class="form-check-input"/>
                            <label for="programInput" name="form-check-label" data-tip data-for="programTip">
                                Program Graph
                            </label>

                            <ReactTooltip id="programTip" place="right" effect="solid">
                                Graphs the desired program (Ex: Computer Science)
                            </ReactTooltip>
                        </div>
                        <div class="form-check">
                            <input id="courseInput" type="radio" name="flexRadioDefault" data-for="courseTip" class="form-check-input"/>
                            <label for="courseInput" name="form-check-label" data-tip data-for="courseTip">
                                Course Graph
                            </label>

                            <ReactTooltip id="courseTip" place="right" effect="solid">
                                Graphs the desired course with all its pre-requsites (Ex: CIS 3760)
                            </ReactTooltip>
                        </div>
                        <div class="form-check">
                            <input id="catalogueInput" type="radio" name="flexRadioDefault" data-for="catalogueTip" class="form-check-input"/>
                            <label for="catalogueInput" name="form-check-label" data-tip data-for="catalogueTip">
                                Catalogue Graph
                            </label>

                            <ReactTooltip id="catalogueTip" place="right" effect="solid">
                                Graphs all the courses/subjects
                            </ReactTooltip>
                        </div>
                    </div>
                </Row>
                <Row>
                    <Form.Group as={Col}>
                        <Form.Label>Desired filename (optional):</Form.Label>
                        <Form.Control type='name' placeholder='Filename' />
                    </Form.Group>
                </Row>
                    
                    
                <Button type='submit'>Makegraph</Button>
            </Form>
    )
}
   

export default MakegraphOption
