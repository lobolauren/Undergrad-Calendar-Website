import React from "react";
import { Button, Card } from "react-bootstrap";

const CourseBlock = ({ code, name, term, weight, description, requiredPrereqs, eqPrereqs, school }) => {
  let graphLink = "/graph/" + school + "/course/" + code;

  const weightFormat = new Intl.NumberFormat('en-US', { 
    minimumIntegerDigits: 1, 
    minimumFractionDigits: 2 
  }); 

  // Create new string for eq_prereqs in the format: [], [], [] where each square bracket is a group of courses related
  // either through 1 OF, 1 OR, etc type prerequisites 
  let newEqPrereqString = "";
  for (let i = 0; i < eqPrereqs.length; i++) {
    newEqPrereqString += "[" + eqPrereqs[i] + "]";

    // ensures no comma on last group of eqprereqs
    if (i < eqPrereqs.length - 1) {
      newEqPrereqString += ", "
    }
  }

  return (
    <Card className="courseblock">
      <Card.Body>

        <Card.Title>{code} - {name}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">
          [{weightFormat.format(weight)}] : {term.join(", ")}
        </Card.Subtitle>
        <Card.Text>{description}</Card.Text>
        {/* Only show the pre-reqs if they aren't empty */}
        {
          (requiredPrereqs.length !== 0) ?
          <Card.Subtitle className="mb-2">{"Required prerequisite(s): " + requiredPrereqs}</Card.Subtitle>
          : ""
        }
        {
          (eqPrereqs.length !== 0) ?
          <Card.Subtitle className="mb-2">{"1 of/or prerequisite(s): " + newEqPrereqString}</Card.Subtitle>
          : ""
        }

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
  requiredPrereqs: "",
  eqPrereqs: ""
};

export default CourseBlock;
