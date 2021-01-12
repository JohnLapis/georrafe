import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Button, FormControl, Form } from 'react-bootstrap';
import Results from '../components/results.jsx';
import { InvalidInputAlert, validateAddress } from '../utils.jsx';

function fetchData() {
  const address = document.querySelector('#address').value;
  if (validateAddress(address)) {
    fetch(`/api/geocode/json?address=${encodeURIComponent(address)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.results.length === 0) {
          ReactDOM.render(
            <div><h4>No locations found.</h4></div>,
            document.querySelector('#results'),
          );
        } else {
          ReactDOM.render(
            <div>
              <h4>Locations:</h4>
              <ul>
                {data.results.map((res) => (
                  <div>
                    <li>Latitude: {res.location.lat}, Longitude: {res.location.lng}</li>
                    <hr/>
                  </div>
                ))}
              </ul>
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

export default function Geocode() {
  return (
    <div>
      <Form className="justify-content-center" inline>
        <FormControl
          id="address"
          size="lg"
          type="text"
          placeholder="Enter address"
        />
        <Button size="lg" onClick={fetchData} variant="outline-success">
          Search Geocode
        </Button>
      </Form>
    </div>
  );
}
