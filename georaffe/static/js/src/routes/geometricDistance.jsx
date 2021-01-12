import React from 'react';
import ReactDOM from 'react-dom';
import {
  Container, Row, Col, Button, FormControl, Form,
} from 'react-bootstrap';
import {
  InvalidInputAlert,
  validateLatitude,
  validateLongitude,
} from '../utils.jsx';

function fetchData() {
  const latitude1 = document.querySelector('#latitude1').value;
  const longitude1 = document.querySelector('#longitude1').value;
  const latitude2 = document.querySelector('#latitude2').value;
  const longitude2 = document.querySelector('#longitude2').value;
  if (validateLatitude(latitude1)
      && validateLongitude(longitude1)
      && validateLatitude(latitude2)
      && validateLongitude(longitude2)) {
    const latlng1 = encodeURIComponent(`${latitude1},${longitude1}`);
    const latlng2 = encodeURIComponent(`${latitude2},${longitude2}`);
    fetch(`/api/geometric-distance/json?latlng=${latlng1}&latlng=${latlng2}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.result === undefined) {
          ReactDOM.render(
            <div><h4>It was not possible to calculate the distance.</h4></div>,
            document.querySelector('#results'),
          );
        } else {
          ReactDOM.render(
            <div>
              <h4>
                Distance:
                {' '}
                {data.result}
                {' '}
                {data.unit}
              </h4>
            </div>,
            document.querySelector('#results'),
          );
        }
      });
  } else {
    ReactDOM.render(
      <InvalidInputAlert />,
      document.querySelector('#results'),
    );
  }
}

export default function GeometricDistance() {
  return (
    <Container>
      <Form className="justify-content-center" inline>
        <Row className="my-4">
          <FormControl
            id="latitude1"
            size="lg"
            type="text"
            placeholder="Enter latitude"
          />
          <FormControl
            id="longitude1"
            size="lg"
            type="text"
            placeholder="Enter longitude"
          />
        </Row>
        <Row>
          <FormControl
            id="latitude2"
            size="lg"
            type="text"
            placeholder="Enter latitude"
          />
          <FormControl
            id="longitude2"
            size="lg"
            type="text"
            placeholder="Enter longitude"
          />
        </Row>
        <Row className="my-4">
          <Button size="lg" onClick={fetchData} variant="outline-success">
            Calculate Geometric Distance
          </Button>
        </Row>
      </Form>
      <Row className="my-4">
        <div id="results" />
      </Row>
    </Container>
  );
}
