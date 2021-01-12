import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Button, FormControl, Form } from 'react-bootstrap';
import Results from '../components/results.jsx';
import { InvalidInputAlert, validateAddress } from '../utils.jsx';

function fetchData() {
  const address = document.querySelector('#address').value;
  if (validateAddress(address)) {
    const params = { address };
    fetch('/api/geocode/json', params)
      .then((data) => data.json())
      .then((data) => {
        ReactDOM.render(
          <Results data={data} />,
          document.querySelector('#results'),
        );
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
