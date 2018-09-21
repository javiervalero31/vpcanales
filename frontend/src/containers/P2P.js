import React, { Component } from 'react';
import axios from 'axios';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import DateTimePicker from 'react-widgets/lib/DateTimePicker';
import moment from 'moment';
import momentLocalizer from 'react-widgets-moment';
import 'react-widgets/dist/css/react-widgets.css';

import Box from '../components/Box';
import {Chart} from '../charts/Chart';
import Header from '../components/Header';
import Home from './../components/Home';
import About from './../components/About';
import NotFound from './../components/NotFound';
import TotalP2P from '../charts/TotalP2P';
import RankingP2P from '../charts/RankingP2P';
import NavBar from './../components/NavBar';


momentLocalizer()

export default class P2P extends Component {
    constructor(props){
        super(props)
        this.state = {
            p2pEndDate: '',
            startDate: moment()
        }
        this.handleChange = this.handleChange.bind(this);
    }
   

    componentDidMount(){
        axios.get("/recargas/api/P2P/recargas_resumen/")
            .then( ({data}) => {
                this.setState({p2pEndDate: data.bounds.max_time, loading: false})
            })
     }

    handleChange(date) {
        this.setState({
          startDate: date
        });
      }
    
    render() {
        let queryUrl = `/recargas/api/P2P/recargas_resumen/?tiempo__fecha__gte=2018-07-01&tiempo__fecha__lte=2018-07-16`
        // const selectionRange = {
		// 	startDate: new Date(),
		// 	endDate: this.state.p2pEndDate,
		// 	key: 'selection',
		// }
        return (
            <div>
                 <Header date={this.state.p2pEndDate} />
                 <BrowserRouter>
                    <Switch>
                        <Route exact path="/recargas/" component={Home} />
                        <Route path="/recargas/about/" component={About} />
                        <Route component={NotFound} />
                    </Switch>
                </BrowserRouter>
                <NavBar />
                {/* <DateRangePicker
                    
                    ranges={[this.state.selectionRange]}
                    onChange={this.handleSelect}
                /> */}
                {/* <div className="col-md-3"> */}
                    
                {/* </div> */}
                <Box title="Venta de Saldo Recargas P2P" color='primary' >
                    <div className="row">
                    <div className="col-md-3">
                        <DateTimePicker
                            // disabled
                            time={false}
                            defaultValue={new Date()}
                        />
                    </div>
                      
                    </div>
                    <div className="col-md-9">
                        <Chart endpoint = {queryUrl} />
                    </div>
                    <div className="col-md-3">
                    
                        <TotalP2P endpoint = {queryUrl} />
                    </div>
                </Box>
                <Box title="Ranking Recargas P2P" color='info' >
                    <RankingP2P endpoint = {queryUrl} />
                </Box>
               
            </div>
        )
    }
}
