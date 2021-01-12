import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Results from '../components/results.jsx'
import {
  InvalidInputAlert,
  validateLatitude,
  validateLongitude
} from '../utils.jsx'
import { Button, FormControl, Form } from 'react-bootstrap'

function fetchData() {
  const latitude = document.querySelector("#latitude").value;
  const longitude = document.querySelector("#longitude").value;
  if (validateLatitude(latitude) && validateLongitude(longitude)) {
    const params = {latlng: `${latitude},${longitude}`}
    fetch("/reverse-geocode/json", params)
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

export default class ReverseGeocode extends Component {
  render() {
    return (
      <div>
        <Form className="justify-content-center" inline>
          <FormControl
            id="latitude"
            size="lg"
            type="text"
            placeholder="Enter latitude"/>
          <FormControl
            id="longitude"
            size="lg"
            type="text"
            placeholder="Enter longitude"/>
          <Button size="lg" onClick={fetchData} variant="outline-success">
            Search Address
          </Button>
        </Form>
      </div>
    )
  }
}
