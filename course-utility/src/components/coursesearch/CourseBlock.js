import React from "react";
import { Button, Card } from "react-bootstrap";

const CourseBlock = ({ code, name, term, weight, description }) => {
  let graphLink = "/graph/course/" + code;

  const weightFormat = new Intl.NumberFormat('en-US', { 
    minimumIntegerDigits: 1, 
    minimumFractionDigits: 2 
  }); 

  return (
    <Card className="courseblock">
      <Card.Body>

        <Card.Title>{code} - {name}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">
          [{weightFormat.format(weight)}] : {term.join(", ")}
        </Card.Subtitle>
        <Card.Text>{description}</Card.Text>

        <Button href={graphLink}>Graph Prerequisites</Button>
      </Card.Body>
    </Card>
  );
};

CourseBlock.defaultProps = {
  code: "",
  name: "",
  term: "",
  weight: "",
  description: "",
};

export default CourseBlock;
