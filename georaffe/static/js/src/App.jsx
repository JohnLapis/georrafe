import React from 'react';
import { Container, Row } from 'react-bootstrap';
import { Switch, Route } from 'react-router-dom';
import Navbars from './components/navbars.jsx';
import Geocode from './routes/geocode.jsx';
import ReverseGeocode from './routes/reverseGeocode.jsx';
import GeometricDistance from './routes/geometricDistance.jsx';

export default function App() {
  return (
    <div>
      <Navbars />
      <Container fluid>
        <Row>
          <Switch>
            <Route path="/geocode" component={Geocode} />
            <Route path="/reverse-geocode" component={ReverseGeocode} />
            <Route path="/geometric-distance" component={GeometricDistance} />
            <Route path="/" component={Geocode} />
          </Switch>
        </Row>
        <Row>
          <div id="results" />
        </Row>
      </Container>
    </div>
  );
}
