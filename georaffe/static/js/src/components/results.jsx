import React, { Component } from 'react';

export default function Results(props) {
  if (Array.isArray(props.data)) {
    if (props.data.status === 'NO_RESULTS') {
      return <div><h4>No results found.</h4></div>;
    }
    return (
      <div>
        <h4>Results:</h4>
        <ul>
          { props.data.map((res) => <li>{res}</li>) }
        </ul>
      </div>
    );
  }
  return (
    <div>
      <h4>
        Result:
        {props.data}
      </h4>
    </div>
  );
}
