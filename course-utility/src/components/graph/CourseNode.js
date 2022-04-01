import { Button, OverlayTrigger, Popover } from 'react-bootstrap'
import { Handle } from 'react-flow-renderer';
import React from 'react';

const handleStyle = {opacity: 0}
const bodystyle = {
  maxHeight: "200px",
  overflowY: "auto"
}

const CourseNode = ({ data }) => {

  const CoursePopup = (
    <Popover>
      <Popover.Header>
        {data.label} - {data.name}
      </Popover.Header>
      <Popover.Body style={bodystyle}>
        <p>{data.description}</p>
      </Popover.Body>
    </Popover>
  );

  return (
    <div className="course-node">
      <OverlayTrigger trigger={['focus']} placement="top" overlay={CoursePopup}>
        <Button variant={data.dropped === true ? 'danger' : data.color}>{data.label}</Button>
      </OverlayTrigger>
      <Handle type='target' position="left" style={handleStyle} />
      <Handle type='source' position="right" style={handleStyle} />
    </div>
  );
}

export default CourseNode;
