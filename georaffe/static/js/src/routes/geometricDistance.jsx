import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Results from '../components/results.jsx'
import {
  Container, Row, Col, Button, FormControl, Form
} from 'react-bootstrap'
import {
  InvalidInputAlert,
  validateLatitude,
  validateLongitude
} from '../utils.jsx'


function fetchData() {
  const latitude1 = document.querySelector("#latitude1").value;
  const longitude1 = document.querySelector("#longitude1").value;
  const latitude2 = document.querySelector("#latitude2").value;
  const longitude2 = document.querySelector("#longitude2").value;
  if (validateLatitude(latitude1)
      && validateLongitude(longitude1)
      && validateLatitude(latitude2)
      && validateLongitude(longitude2)) {
    const params = {
      latlng1: `${latitude1},${longitude1}`,
      latlng2: `${latitude2},${longitude2}`
    }
    fetch("/api/geometric-distance/json", params)
      .then(data => data.json())
      .then(data => {
        ReactDOM.render(
          <Results data={data}/>,
          document.querySelector('#results')
        )
      })
  } else {
    ReactDOM.render(
      <InvalidInputAlert/>,
      document.querySelector('#results')
    )
  }
}

export default class GeometricDistance extends Component {
  render() {
    return (
      <div>
        <Form className="justify-content-center" inline>
          <Container>
            <Row>
              <FormControl
                id="latitude1"
                size="lg"
                type="text"
                placeholder="Enter latitude"/>
              <FormControl
                id="longitude1"
                size="lg"
                type="text"
                placeholder="Enter longitude"/>
            </Row>
            <Row>
              <FormControl
                id="latitude2"
                size="lg"
                type="text"
                placeholder="Enter latitude"/>
              <FormControl
                id="longitude2"
                size="lg"
                type="text"
                placeholder="Enter longitude"/>
            </Row>
            <Row>
              <Button size="lg" onClick={fetchData} variant="outline-success">
                Calculate Geometric Distance
              </Button>
            </Row>
          </Container>
        </Form>
      </div>
    )
  }
}
