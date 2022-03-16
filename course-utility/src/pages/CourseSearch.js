import React, { useState, useEffect } from 'react'
import axios from 'axios';

import { Form, Button, Row, Col } from 'react-bootstrap'
import { Container } from 'react-bootstrap'
import SearchForm from '../components/coursesearch/SearchForm'
import ResultsTable from '../components/coursesearch/ResultsTable'
import InfoModal from '../components/coursesearch/InfoModal'
import SortOptions from '../components/coursesearch/SortOptions'

const CourseSearch = () => {

    // get the data with the given search params
    const fetchData = async (param) => {
        axios.get(global.config.base_url + '/courses', { params: param }).then((res) => {
            setCourses(res.data);
        }, (err) => { // and error occured
            console.log(err);
        });
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        let courseName = event.target.courseName.value;
        let courseCode = event.target.courseCode.value;
        let courseWeight = event.target.courseWeights.value;
        let isFallSelected = event.target.fallCheckbox.checked;
        let isWinterSelected = event.target.winterCheckbox.checked;
        let isSummerSelected = event.target.summerCheckbox.checked;

        // get terms selected
        let terms = buildTermsList(isFallSelected, isWinterSelected, isSummerSelected);

        let courseSearchQuery = {
            "name": courseName,
            "code": courseCode,
            "weight": courseWeight,
            "terms": terms.toString() // convert to string because array causes issues with axios params
        }

        // get the input data from the server
        fetchData(courseSearchQuery);
    }

    // builds a list out of the check boxes for term NOTE: MUST UPDATE API TO WORK WITH THIS
    function buildTermsList(isFallSelected, isWinterSelected, isSummerSelected) {
        let terms = [];
        if (isFallSelected)
            terms.push("F");
        if (isWinterSelected)
            terms.push("W");
        if (isSummerSelected)
            terms.push("S");
        
        return terms.length === 0 ? ["F", "W", "S"] : terms;
    }
    
    // hook containing courses
    const [courses, setCourses] = useState();

    return (
        <Container className="mt-5">
            <h2>Course Search <InfoModal/></h2>
            <SearchForm handler={handleSubmit}/>
            <SortOptions />
            <br/>

            <ResultsTable courses={courses}/>
        </Container>
    )
}

export default CourseSearch
