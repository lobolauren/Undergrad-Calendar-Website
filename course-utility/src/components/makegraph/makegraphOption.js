import React from 'react';
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import { solid, regular, brands } from '@fortawesome/fontawesome-svg-core/import.macro'
import { Form, Button, Row, Col } from 'react-bootstrap'

const MakegraphOption=()=>{
    return (
        
            <Form bg="dark" expand="lg" variant="dark">
                
                <Row>
                    <div className='termBox'>
                    <link rel="stylesheet" type="text/css" href="bootstrap/dist/css/bootstrap.min.css" />
                    <link rel="stylesheet" type="text/css" href="https://netdna.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" />
                    <link rel="stylesheet" type="text/css" href="https://flatlogic.github.io/awesome-bootstrap-checkbox/demo/build.css" />
                        <div class="checkbox  checkbox-circle">
                            <input id="chkDefault" type="checkbox"/>
                            <label for="chkDefault">
                                Department Graph
                            </label>
                        </div>
                        <div class="checkbox  checkbox-circle">
                            <input id="chkDefault" type="checkbox"/>
                            <label for="chkDefault">
                                Program Graph
                            </label>
                        </div>
                        <div class="checkbox  checkbox-circle">
                            <input id="chkDefault" type="checkbox"/>
                            <label for="chkDefault">
                                Course Graph
                            </label>
                        </div>
                        <div class="checkbox  checkbox-circle">
                            <input id="chkDefault" type="checkbox"/>
                            <label for="chkDefault">
                                Catalogue Graph
                            </label>
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
