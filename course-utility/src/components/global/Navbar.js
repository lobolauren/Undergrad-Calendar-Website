import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap'

const _Navbar = () => {
  return (
    <Navbar bg="dark" expand="lg" variant="dark" className='nav'>
      <Container>
        <Navbar.Brand href="#home">Guelph Course Utility</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/coursesearch">Course Search</Nav.Link>
            <Nav.Link href="/makegraph">Make Graph</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default _Navbar;
