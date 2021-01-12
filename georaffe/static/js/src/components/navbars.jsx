import React from 'react';
import { Nav, Navbar } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

export default function () {
  return (
    <Navbar bg="light" expand="sm">
      <Navbar.Brand className="font-weight-bold" href="">Georaffe</Navbar.Brand>
      <Nav variant="pills" defaultActiveKey="/geocode">
        <LinkContainer to="/geocode">
          <Nav.Link>Geocode</Nav.Link>
        </LinkContainer>
        <LinkContainer to="/reverse-geocode">
          <Nav.Link>Reverse Geocode</Nav.Link>
        </LinkContainer>
        <LinkContainer to="/geometric-distance">
          <Nav.Link>Geometric Distance</Nav.Link>
        </LinkContainer>
      </Nav>
    </Navbar>
  );
}
