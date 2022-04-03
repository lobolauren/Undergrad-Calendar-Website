import React from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

import { Container } from "react-bootstrap";
import InfoModal from "../components/makegraph/InfoModal";
import MakeGraphForm from "../components/makegraph/MakeGraphForm";

const MakeGraph = () => {
  
  // Clear potential course name from home search
  localStorage.clear();
  
  const navigate = useNavigate();

  const [selectedDept, setSelectedDept] = useState();

  const handleSubmit = (event) => {
    event.preventDefault();

    let minorValue = false;
    let graphType = event.target.graphType.value;
    let courseCode = '';
    let school = event.target.courseSearchSchoolId.value;

    let graphWanted = {};
    let checkHold;
    let completeCode;

    if (graphType === "program") {
      minorValue = event.target.minorId.checked;
      graphWanted = {
        type: graphType,
        code: selectedDept,
        minor: minorValue,
      };

    } else if (graphType === 'course') {

      courseCode = event.target.courseCode.value;
      completeCode = selectedDept + '*' + courseCode;

      graphWanted = {
        school: school,
        type: graphType,
        code: completeCode,
      };

    } else {

      graphWanted = {
        school: school,
        type: graphType,
        code: selectedDept,
      };

    }

    if (graphWanted["type"] === "course" || graphWanted["type"] === "department") {

      //make call to check if page exists
      let courseSearchQuery = {
        school: graphWanted["school"],
        name: "",
        code: completeCode,
        weight: "all",
        terms: "F,W,S", // convert to string because array causes issues with axios params
      };

      axios.get(global.config.base_url + "/courses", { params: courseSearchQuery }).then((res) => {
        checkHold = Object.keys(res.data).length;

        // navigates to a separate page to display the desired graph
        if (graphWanted["type"] === "course") {
          if (checkHold === 1) {
            navigate(
              `/graph/${graphWanted["school"]}/${graphWanted["type"]}/${graphWanted["code"]}`);
          } else {
            alert("Invalid input. Could not graph.");
          }
        } else if (graphWanted["type"] === "department") {
          if (checkHold > 1) {
            navigate(`/graph/${graphWanted["school"]}/${graphWanted["type"]}/${graphWanted["code"]}`);
          } else {
            alert("Invalid input. Could not graph.");
          }
        }
      },
      (err) => {
        // an error occured
        console.log(err);
      });
    } else if (graphWanted["type"] === "program") {

      axios.get(global.config.base_url + "/get_programs_list", {}).then((res) => {
        checkHold = false;

        for (let i = 0; i < Object.keys(res.data["programs"]).length; i++) {
          if (graphWanted["code"].toLowerCase() === res.data["programs"][i].toLowerCase()) {
            checkHold = true;
          }
        }
        
        console.log(checkHold);
        if (checkHold === true) {
          if (graphWanted["minor"] === true) {
            navigate(`/graph/${graphWanted["type"]}/minor/${graphWanted["code"]}`);
          } else if (graphWanted["minor"] === false) {
            navigate(`/graph/${graphWanted["type"]}/${graphWanted["code"]}`);
          }
        } else {
          alert("Invalid input. Could not graph.");
        }
      },
      (err) => {
        // an error occured
        console.log(err);
      });
    }
  };

  return (
    <Container className="mt-5">
      <h2>Make Graph<InfoModal /></h2>
      <MakeGraphForm handler={handleSubmit} setSelectedDept={setSelectedDept} />
    </Container>
  );
};

export default MakeGraph;
