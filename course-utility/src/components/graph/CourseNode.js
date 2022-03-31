import { Button, OverlayTrigger, Popover } from 'react-bootstrap'
import { Handle, Node, Edge } from 'react-flow-renderer';
import React, { useCallback } from 'react';

const handleStyle = {opacity: 0}
const bodystyle = {
  maxHeight: "200px",
  overflowY: "auto"
}

const CourseNode = ({ data }) => {

  const simulateDropButtonClick = () => {
    data.simulateDrop(data.id);
  }

  const CoursePopup = (
    <Popover>
      <Popover.Header>
        {data.label} - {data.name}
      </Popover.Header>
      <Popover.Body style={bodystyle}>
        <p>{data.description}</p>
        { data.courseSearched
        ? null
        : <Button variant='danger' onClick={simulateDropButtonClick}>Simulate Drop</Button>}
      </Popover.Body>
    </Popover>
  );

  return (
    <div className="course-node">
      <OverlayTrigger trigger={['focus']} placement="top" overlay={CoursePopup}>
        <Button variant={data.color}>{data.label}</Button>
      </OverlayTrigger>
      <Handle type='target' position="left" style={handleStyle} />
      <Handle type='source' position="right" style={handleStyle} />
    </div>
  );
}

export default CourseNode;
