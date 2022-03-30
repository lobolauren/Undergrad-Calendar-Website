import React from 'react';
import { Button, Popover } from 'react-bootstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro'

const Popup = ({ course }) => {

  // return (
  //   <Popover>
  //       <Popover.Header>
  //           {course.code}
  //           {/* {course.code} - {course.name} */}
  //       </Popover.Header>
  //       <Popover.Body>
  //           {/* <p>{course.description}</p> */}
  //           <Button variant='danger'>Simulate Drop</Button>
  //       </Popover.Body>
  //   </Popover>
  // );

  return (
    <Popover>
        <Popover.Header>
            cis 3490
            {/* {course.code} - {course.name} */}
        </Popover.Header>
        <Popover.Body>
            {/* <p>{course.description}</p> */}
            <Button variant='danger'>Simulate Drop</Button>
        </Popover.Body>
    </Popover>
  );
}

export default Popup