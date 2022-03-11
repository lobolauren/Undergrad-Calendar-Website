import React from 'react'

const CourseBlock = ({ code, name, term, weight, description }) => {
  return (
    <div className='courseblock'>
        <span>{code} - {name} [{weight}] : {term}</span>
        <p>{description}</p>
    </div>
  )
}

CourseBlock.defaultProps = {

    code: '',
    name: '',
    term: '',
    weight: '',
    description: ''

}

export default CourseBlock