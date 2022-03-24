import React, { useState, useEffect } from 'react'
import axios from 'axios';

import { Form, Button, Row, Col } from 'react-bootstrap'
import { Container } from 'react-bootstrap'
import SearchForm from '../components/coursesearch/SearchForm'
import ResultsTable from '../components/coursesearch/ResultsTable'
import InfoModal from '../components/coursesearch/InfoModal'
import SortOptions from '../components/coursesearch/SortOptions'

let sortType = "courseCodeOption";
let sortOrder = "ascending";

const CourseSearch = () => {

    // get the data with the given search params
    const fetchData = async (param) => {
        axios.get(global.config.base_url + '/courses', { params: param }).then((res) => {

            // no courses were found
            if (res.data.length == 0) {
                // Reset courses to initial state, so it shows no courses found
                setCourses(null);
                return;
            }

            // leave as is if courseCodeOption is picked. Otherwise, sort by name
            let correctSortedOrder = (sortType == "courseCodeOption" ? res.data : sortResultsByCustomType(res.data, "name"));

            if (sortOrder == "descending") {// && sortType == "courseCodeOption") {
                let reversedCopy = correctSortedOrder.reverse();
                setCourses(reversedCopy);
            }
            else {
                setCourses(correctSortedOrder);
            }
            
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
        let isGuelphSelected = event.target.courseSearchSchoolId.value;
        // get terms selected
        let terms = buildTermsList(isFallSelected, isWinterSelected, isSummerSelected);

        let courseSearchQuery = {
            "school":isGuelphSelected,
            "name": courseName,
            "code": courseCode,
            "weight": courseWeight,
            "terms": terms.toString() // convert to string because array causes issues with axios params
        }

        // get the input data from the server
        fetchData(courseSearchQuery);
    }

    // builds a list out of the check boxes for term
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

    // sorts the passed in courses by the specified type alphabetically
    const sortResultsByCustomType = (courses, type) => {
        if (courses == null) return;

        // sort by passed in type
        let courses_copy = courses.slice();
        courses_copy.sort(function(a, b) {
            if(a[type] < b[type]) { return -1; }
            if(a[type] > b[type]) { return 1; }
            return 0;
        })
        return courses_copy;
    }

    // reverses the set courses
    const reverseCourseOrder = () => {
        if (courses == null) return;

        let courses_copy = courses.slice();
        courses_copy.reverse();
        setCourses(courses_copy);
    }

    // sorts by the correct sort type when the dropdown option is selected
    function updateSortTypeOption(event) {
        event.preventDefault();

        // update stored sort type
        sortType = event.target.value;

        // sort by that type and take into consideration the order (ascending or descending)
        if (sortType == "courseNameOption") {
            let sortedCourses = sortResultsByCustomType(courses, "name")
            sortOrder == "ascending" ? setCourses(sortedCourses) : setCourses(sortedCourses.reverse());
        }
        else { // sort by course code
            let sortedCourses = sortResultsByCustomType(courses, "code")
            sortOrder == "ascending" ? setCourses(sortedCourses) : setCourses(sortedCourses.reverse());
        }
    }

    // called when the new sort order is changed
    function updateSortOrderOption(event) {
        event.preventDefault();

        // update selected sort order and reverse
        sortOrder = event.target.value;
        reverseCourseOrder();
    }
    
    // hook containing courses
    const [courses, setCourses] = useState();

    return (
        <Container className="mt-5">
            <h2>Course Search <InfoModal/></h2>
            <SearchForm handler={handleSubmit}/>
            <SortOptions sortTypeHandler={updateSortTypeOption} sortOrderHandler={updateSortOrderOption}/>
            <br/>

            <ResultsTable courses={courses}/>
        </Container>
    )
}

export default CourseSearch
