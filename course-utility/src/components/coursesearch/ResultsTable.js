import React from 'react'
import CourseBlock from './CourseBlock'

const ResultsTable = ({courses}) => {
    return (
        <div className='resultsTable'>
            {
                courses ? 
                    React.Children.toArray(
                        courses.map(
                            (course) => (
                                <CourseBlock code={course.code} name={course.name} weight={course.weight} term={course.term} description={course.desc} />
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