import React from 'react';
import { Modal, Button } from 'react-bootstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { solid, regular, brands } from '@fortawesome/fontawesome-svg-core/import.macro'

function InfoModal() {
  const [show, setShow] = React.useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <Button variant="link" onClick={handleShow}>
        <FontAwesomeIcon icon={solid('circle-info')} size="lg" color="black" />
      </Button>

      <Modal show={show} onHide={handleClose} size="lg">
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">Limitations</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <ul>
            <li>
              The graph won't indicate when courses require you to pick more then one of a group of 
              courses. (ie. 2 of course A, course B, course C)
            </li>
            <li>
              The graph won't indicate if a course has a single prerequisite could alternatively be 
              replaced by a group of prerequisites. (ie. course A or (course B and course C))
            </li>
            <li>
              The graph may indicate that there are more then on equivalent prerequisites but only 
              show one. This happens because the other courses may not longer exist or the prerequisite 
              isn't a specific University of Guelph Course (ie. course A or experience in field)
            </li>
          </ul>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={() => {}}>Close</Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default InfoModal