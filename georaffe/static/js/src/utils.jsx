import React, { Component } from 'react';
import { Alert } from 'react-bootstrap';

export class InvalidInputAlert extends Component {
  constructor(props, context) {
    super(props, context);
    this.handleDismiss = this.handleDismiss.bind(this);
    this.state = {
      show: true,
    };
  }

  handleDismiss() {
    this.setState({ show: false });
  }

  render() {
    if (this.state.show) {
      return (
        <Alert variant="warning" onClose={this.handleDismiss} dismissible>
          <p>Invalid input.</p>
        </Alert>
      );
    }
    return null;
  }
}

export function validateAddress(address) {
  return address !== '';
}

export function validateLatitude(lat) {
  return lat !== ''
    && !Number.isNaN(Number(lat))
    && Number(lat) >= -90
    && Number(lat) <= 90;
}

export function validateLongitude(lng) {
  return lng !== ''
    && !Number.isNaN(Number(lng))
    && Number(lng) >= -180
    && Number(lng) <= 180;
}
