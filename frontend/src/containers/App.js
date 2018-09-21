import React, { Component } from 'react';
import P2P from './P2P';

// import logo from './logo.svg';
// import {DimensionList} from './components/DimensionList';

import '../App.css';
// import {Route, Switch, BrowserRouter} from 'react-router-dom';
// import Home from './components/Home';
// import NotFound from './components/NotFound';
// import About from './components/About';


class App extends Component {
 
 
  render() {
    return (
      <div className="App">
        <h1>Portal de Recargas</h1>
        <P2P />
        

        {/* <h4 className="text-aqua" id='dataDate'>Obteniendo datos...</h4> */}
        {/* <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Bienvenido a las Recargas</h1>
        </header> */}
              
        {/* <Box title="Recargas de Saldo P2P" color='primary' /> */}
        {/* <Box title="Ranking de Saldo P2P" /> */}
        {/* <DataProvider 
          endpoint="/recargas/api/P2P/recargas_resumen/?tiempo__fecha__gte=2018-05-01&tiempo__fecha__lte=2018-05-22" 
          render={data => <Box 
                            title="Venta de Recargas P2P por fecha" 
                            data={data.direcciones} 
                            body={
                              <Chart
                                endpoint ="/recargas/api/P2P/recargas_resumen/?tiempo__fecha__gte=2018-04-01&tiempo__fecha__lte=2018-05-10"
                              />
                            } 
                          />
                  } 
        /> */}
        {/* <DimensionList nombres={[{id: 3, nombre: "DESJERARQUIZADO"}, {id: 2, nombre: "ESTE"}, {id: 1, nombre: "OESTE"}]} /> */}
        

        {/* <BrowserRouter>
          <Switch>
            <Route exact path="/recargas/" component={Home} />
            <Route path="/recargas/about/" component={About} />

            <Route component={NotFound} />
          </Switch>
        </BrowserRouter> */}
      </div>
    );
  }
}

export default App;
