import React, { useState, useEffect } from 'react'
import axios from 'axios';

import { Container } from 'react-bootstrap'
import SearchForm from '../components/coursesearch/SearchForm'
import ResultsTable from '../components/coursesearch/ResultsTable'
import InfoModal from '../components/coursesearch/InfoModal'

const CourseSearch = () => {

    const testSubmitData = {
        name: 'test',
        code: '3760',
        weight: '0.5',
        term: 'W'
    }

    
    const [courses, setCourses] = useState();
    
    useEffect(() => {
        // get the data with the given search params
        const fetchData = async () => {
            axios.get(global.config.base_url + '/courses', { params: testSubmitData }).then((res) => {
                console.log(res.data);
                setCourses([res.data]);
            }, (err) => { // and error occured
                console.log(err);
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
