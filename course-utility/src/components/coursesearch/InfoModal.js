import React from 'react';
import { Modal, Button } from 'react-bootstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro'

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
          <Modal.Title id="contained-modal-title-vcenter">Notes</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <ul>
            <li>
              Courses are from the 2021-2022 Academic calendar year which is accessed <a href="https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/">here</a>.
            </li>
            <li>
            When searching course weights, you can either search for all course weights, or you can search for one specific course weight.
            </li>
          </ul>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={handleClose}>Close</Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default InfoModal