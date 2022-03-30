import React from 'react';

import '../../styles/graph.css'

const Legend = () => {

  return (
    <div className="legend p-3">
        <p>Required prerequisite</p>
        <div className="solidLine"/>
        
        <p>'One of' prerequisite</p>
        <div className="dottedLine"/>
        
        <p>Searched course</p>
        <div className="searchCourseRect"/>

        <p>Course in same department</p>
        <div className="sameDepartmentRect"/>

        <p>Course in different department</p>  
        <div className="differentDepartmentRect"/>
    </div>
  );
}

export default Legend