import React from 'react'
import CourseBlock from './CourseBlock'

const ResultsTable = ({courses}) => {
    console.log("Courses from ResultsTable", courses);
    // console.log("Length = " + courses.length);
    if (courses != null) {
        console.log("Course = ", courses[0]);
    }

    return (
        <div className='resultsTable'>
            {
                courses ? 
                    React.Children.toArray(
                        courses.map(
                            (course) => (
                                <CourseBlock code={course.code} name={course.name} weight={course.weight} term={course.term} description={course.description} />
                            )
                        )
                    )
                :
                <span>No Courses to Display...</span>
            }
        </div>
    )
}

export default ResultsTable