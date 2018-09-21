import React, { Component } from 'react'
import moment from 'moment';
import 'moment/locale/es';

export default class Header extends Component {

    render() {
        let ultimaFecha = moment(this.props.date);
        return (
            <div>
                {
                    this.props.date ?
                    <h4 style={{color: '#00c0ef'}}> Data actualizada hasta el {ultimaFecha.format('DD')} de {ultimaFecha.format('MMMM')} de {ultimaFecha.year()}.</h4> 
                    : <h4>Sin datos</h4>
                }

                {/* <p style={{color: 'blue'}}>{ultimaFecha.format('YYYY-MM-DD')}</p> */}
            </div>
        )
    }
}
 