import React, { Component } from "react";
import PropTypes from "prop-types";

class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired
  };

  state = {
      data: [],
      loaded: false,
      placeholder: "Cargando..."
    };

  componentDidMount() {
    fetch(this.props.endpoint)
      .then(response => {
        // if (response.status !== 200) {
        //   return this.setState({ placeholder: "Algo salio mal." });
        // }
        return response.json();
      })
      .then(
          data => {
            console.log(data);
            this.setState({ data: data.direcciones, loaded: true })
            console.log('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO');
            console.log(this.state.data);
            console.log('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO');
          }
        );
  }

  render() {
    const { data, loaded, placeholder } = this.state;
    return loaded ? this.props.render(data) : <p>{placeholder}</p>;
  }
}

export default DataProvider;