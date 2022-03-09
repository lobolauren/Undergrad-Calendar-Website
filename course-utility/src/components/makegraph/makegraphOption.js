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
                        <div class="checkbox  checkbox-circle">
                            <input id="chkDefault" type="checkbox" data-tip data-for="departmentTip"/>
                            <label for="chkDefault" data-tip data-for="departmentTip">
                                Department Graph
                            </label>

                            <ReactTooltip id="departmentTip" place="right" effect="solid">
                                Tooltip for the department graph style
                            </ReactTooltip>
                        </div>
                        <div class="checkbox  checkbox-circle">
                            <input id="chkDefault" type="checkbox" data-tip data-for="programTip"/>
                            <label for="chkDefault" data-tip data-for="programTip">
                                Program Graph
                            </label>

                            <ReactTooltip id="programTip" place="right" effect="solid">
                                Tooltip for the program graph style
                            </ReactTooltip>
                        </div>
                        <div class="checkbox  checkbox-circle">
                            <input id="chkDefault" type="checkbox" data-tip data-for="courseTip"/>
                            <label for="chkDefault" data-tip data-for="courseTip">
                                Course Graph
                            </label>

                            <ReactTooltip id="courseTip" place="right" effect="solid">
                                Tooltip for the course graph style
                            </ReactTooltip>
                        </div>
                        <div class="checkbox  checkbox-circle">
                            <input id="chkDefault" type="checkbox" data-tip data-for="catalogueTip"/>
                            <label for="chkDefault" data-tip data-for="catalogueTip">
                                Catalogue Graph
                            </label>

                            <ReactTooltip id="catalogueTip" place="right" effect="solid">
                                Tooltip for the catalogue graph style
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
