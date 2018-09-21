import React from 'react'


export default class Button extends React.Component {
	state = { counter: 0};
  
  handleClick = () => {
  	// this.state.counter++ // Do not mutate state directly. Use setState()
    this.setState({ 
    	counter: this.state.counter + 1
      })
  };
  
  render() {
  	return (
    	<button onClick={this.handleClick}>
        <span>{this.props.label}<br/></span>
				{this.state.counter}
      </button>
    );
  }
}