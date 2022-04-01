import { Button, OverlayTrigger, Popover } from 'react-bootstrap'
import { Handle, Node, Edge } from 'react-flow-renderer';
import React, { useCallback } from 'react';

const handleStyle = {opacity: 0}
const bodystyle = {
  maxHeight: "200px",
  overflowY: "auto"
}

const CourseNode = ({ data }) => {

  const simulateDropButtonClick = useCallback(() => {
    data.updateDrop(data.id, 1);
  });

  const simulateUndropButtonClick = useCallback(() => {
    data.updateDrop(data.id, -1);
  });

  const CoursePopup = (
    <Popover>
      <Popover.Header>
        {data.label} - {data.name}
      </Popover.Header>
      <Popover.Body style={bodystyle}>
        <p>{data.description}</p>
        {!data.courseSearched
        ? <Button 
            variant={data.dropValue > 0 ? 'success' : 'danger'}
            onClick={data.dropValue > 0 ? simulateUndropButtonClick : simulateDropButtonClick}
          >
            {data.dropValue > 0 ? 'Undrop' : 'Simulate Drop'} 
          </Button>
        : null} 
      </Popover.Body>
    </Popover>
  );

  return (
    <div className="course-node">
      <OverlayTrigger trigger={['focus']} placement="top" overlay={CoursePopup}>
        <Button variant={data.dropValue > 0 ? 'danger' : data.color}>{data.label}</Button>
      </OverlayTrigger>
      <Handle type='target' position="left" style={handleStyle} />
      <Handle type='source' position="right" style={handleStyle} />
    </div>
  );
}

export default CourseNode;
