import React, { useState } from 'react'
import { Container } from 'react-bootstrap'
import SearchForm from '../components/SearchForm'
import ResultsTable from '../components/ResultsTable'

const CourseSearch = () => {

    const [courses, setCourses] = useState([

        {
            code: 'CIS*3760',
            name: 'Gregory',
            weight: '1.0',
            term: 'W',
            desc: 'String parsing mostly...'
        },
        {
            code: 'CIS*1000',
            name: 'Intro to Bees',
            weight: '1000000.0',
            term: 'P',
            desc: 'According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don\'t care what humans think is impossible.'
        }

    ]);

    return (
        <Container className="mt-40">
            <h3>Course Search</h3>
            <SearchForm/>

            <br/>

            <ResultsTable courses={courses}/>
        </Container>
    )
}

export default CourseSearch