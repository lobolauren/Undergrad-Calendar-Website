import React, { useState, useEffect } from 'react'
import axios from 'axios';

import { Container } from 'react-bootstrap'
import SearchForm from '../components/coursesearch/SearchForm'
import ResultsTable from '../components/coursesearch/ResultsTable'
import InfoModal from '../components/coursesearch/InfoModal'

const CourseSearch = () => {

    const [courses, setCourses] = useState();

    useEffect(() => {

        const fetchData = async () => {
            axios.get(global.config.base_url + '/coursestest').then((res) => {
                setCourses(res.data);
            });
        }
        fetchData();
    }, []);

    return (
        <Container className="mt-40">
            <h3>Course Search <InfoModal/></h3>
            <SearchForm/>

            <br/>

            <ResultsTable courses={courses}/>
        </Container>
    )
}

export default CourseSearch
