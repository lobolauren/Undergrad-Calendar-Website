import React from "react";
import CourseBlock from "./CourseBlock";

const ResultsTable = ({ courses, school }) => {
  return (
    <div className="resultsTable">
      {courses ? (
        React.Children.toArray(
          courses.map((course) => (
            <CourseBlock
              code={course.code}
              name={course.name}
              weight={course.weight}
              term={course.terms}
              description={course.description}
              school={school}
              requiredPrereqs={course.prereqs["reg_prereqs"]}
              eqPrereqs={course.prereqs["eq_prereqs"]}
            />
          ))
        )
      ) : (
        <span>No Courses to Display...</span>
      )}
    </div>
  );
};

export default ResultsTable;
