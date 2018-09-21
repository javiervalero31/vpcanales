import React from 'react';
import {shallow} from 'enzyme';
import App from '../App';

describe("App", function(){

  it('renders without crashing', () => {
    let mountedApp = shallow(<App />);
  });
  
  
  it('renders P2P', () => {
    let mountedApp = shallow(<App />);
    const locators = mountedApp.find('P2P');
    expect(locators.length).toBe(1);
  });


});


// import React from 'react';
// import ReactDOM from 'react-dom';
// import App from './App';

// it('renders without crashing', () => {
//   const div = document.createElement('div');
//   ReactDOM.render(<App />, div);
//   ReactDOM.unmountComponentAtNode(div);
// });
