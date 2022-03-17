import React from 'react'
import { Button, Card } from 'react-bootstrap'

const CourseBlock = ({ code, name, term, weight, description }) => {

  let graphLink = '/graph/course/'+code

  return (
        <Card className='courseblock'>

          <Card.Body>

            <Card.Title>{code} - {name} [{weight}] : {term}</Card.Title>
            <Card.Text>{description}</Card.Text>

            <Button href={graphLink}>Graph Prerequisites</Button>
          </Card.Body>
          
        </Card>
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