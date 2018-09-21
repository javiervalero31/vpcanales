import React, {Component} from 'react'
import AmCharts from '@amcharts/amcharts3-react'
import axios from 'axios'


export default class Chart extends Component{
    constructor(props){
        super(props)
        this.state = {
            loading: true,
            dataProvider:[],
        }
    }
    
    componentDidMount(){
        axios.get(this.props.endpoint).then( ({data}) => {
            const result = []
            data.totales.total = 'Total'
            result.push(data.totales)
            this.setState({dataProvider: result, loading: false})
            console.log('===================T================');
            console.log(data.totales);
            console.log('Result', result);
            
            console.log(this.state.dataProvider);
            console.log('===================T================');
        })
        
    }
    
    // shouldComponentUpdate(nextProps, nextState) {
    //     this.setState({dataProvider: nextProps})
    // }
        
    render() {
        
        if (this.state.loading){
            return <div>
                        <h2>Cargando...</h2>
                   </div>
        } else {
        
        const ventaColor = '#014266';
        const cuotaColor = '#00C0EF';

        const config = {"titles":[{"id":"total-acum", "text":"Act. Acumulada"}],
        "startDuration": 2,
        "fontSize": 13,
        "color": "#B7B7B7",
        "decimalSeparator": ",",
        "thousandsSeparator": ".",
        "maxSelectedSeries": 5,
        // "axisColor": "#555555",
        // "fillColor": "#555555",
        
        // MARGINGS
        "autoMargins": false,
        "marginLeft": 0,
        "marginRight": 0,
        "marginTop": 40,
        "marginBottom": 25,
        "theme": "light",
        "type": "serial",
        "dataProvider": this.state.dataProvider,
        "categoryField": "total",
        "depth3D": 20,
        "angle": 30,
        "categoryAxis": {
            "labelRotation": 0,
            "gridPosition": "start",
            "gridAlpha": 0,
            "axisAlpha": 0
          },
          "valueAxes": [ {
            "stackType": "none",
            // "position": "left",
            "fontSize": 10,
            // "stackType": "100%",
            // "title": "%",
            "minimum": 0,
            // "autoGridCount": false,
            // "gridCount": 1,
            // "labelFrequency": 2,
    
            "capMaximum": 10,
            "capMinimum": 0,
            // "startOnAxis": true,
            "color": "#B7B7B7",
            // "labelFunction": function(valueText, date, categoryAxis) {
            //     return date.toLocaleDateString();
            //   },
            // "dashLength": 2,
            // "gridAlpha": 0,
            "axisAlpha": 0.21,
            // "axisAlpha": 0.21,
            // "unit": "Bs.F",
            "axisTitleOffset": 12,
            // "axisTitleOffset": 100,
            // "id": "ValueAxis-1",
            "axisColor": "#8E8E8E",
            "gridColor": "#FFFFFF",
            "tickLength": 0,
          } ],
        
          "graphs": [ {
            "title": 'Total Ventas:',
            "valueField": "total_venta",
            "lineColor": ventaColor,
            // "labelText": "[[percents]]%",
            "color": "#fff",
            "type": "column",
            "lineAlpha": 0.75,
            "fillAlphas": 0.7,
            "showBalloon": true,
            },{
            "valueField": "total_cuota",
            "title":'Total Cuota:',
            "type": "column",
            "lineAlpha": 0.75,
            "fillAlphas": 0.7,
            "showBalloon": true,
            // "labelText": "[[percents]]%",
            "color": "#fff",
            "lineColor": cuotaColor,
            "negativeFillColors": "#289eaf",
            "negativeLineColor": "#289eaf"
            },{
            "title": "Cumplimiento (%):",
            // "unit": '%',
            "valueField": "cumplimiento",
            "accessibleLabel": "",
            "balloonText": "",
            "bullet": "round",
            "bulletBorderColor": "#000000",
            "color": "#000000",
            "customMarker": "",
            "fontSize": 0,
            "gapPeriod": 0,
            "includeInMinMax": false,
            "labelText": "",
            "legendAlpha": 0,
            "legendColor": "#000000",
            "lineAlpha": 0,
            "lineColor": "#000000",
            "lineThickness": 0,
            "markerType": "triangleUp",
            "switchable": false,
            "type": "ohlc"
            }
          ],
        "legend": {
            // "enabled": false,
            "align": "center",
            "bottom": 0,
            "color": "#6D6D6D",
            // "autoMargins": false,
            "equalWidths": false,
            "fontSize": 12,
            "labelText": "[[title]]",
            "right": 0,
            "rollOverColor": "#6D6D6D",
            "spacing": 60,
            "switchType": "v",
            "top": 0,
            "valueAlign": "left",
            // "valueWidth": 0,
            // "useGraphSettings": true,
            "verticalGap": 10
        },
        "chartCursor": {
            "categoryBalloonEnabled": false,
            "cursorAlpha": 0,
            "zoomable": false
          },
        // "export": {
        //     "enabled": true,
        //     "fileName": "Totales",
        //     "columnNames": {
        //         "total_venta": "Venta Acumulada",
        //         "total_cuota": "Cuota Acumulada",
        //         "cumplimiento": "% Cumplimiento"
        
        //     }}
    }


        return (
            <div>
                <AmCharts.React style={{ width: "100%", height: "500px"}} options={config} />
            </div>
           
        )
    }
    }
}

