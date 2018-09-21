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
            this.setState({dataProvider: data.part_direction, loading: false})
            console.log(data.part_direction)
            console.log(this.state.dataProvider)
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

        const config = {
            "theme": "light",
            "type": "serial",
            "language": "es",
            "decimalSeparator": ",",
            "thousandsSeparator": ".",
            "startDuration": 2,
            "dataProvider": this.state.dataProvider,
            "depth3D": 20,
            "legend": {
              "align": "center",
              "bottom": 0,
              "color": "#6D6D6D",
              "autoMargins": false,
              "equalWidths": false,
              "fontSize": 12,
              "labelText": "[[title]]",
              "right": 0,
              "rollOverColor": "#6D6D6D",
              "spacing": 60,
              // "switchType": "v",
              "top": 0,
              "valueAlign": "left",
              // "valueWidth": 0,
              // "useGraphSettings": true,
              // "verticalGap": 10
            },
            // "synchronizeGrid":true,
            "categoryField": "direccion__nombre", // This will change accord with the API
            // "depth3D": 20,
            "angle": 30,
          
            "categoryAxis": {
              "labelRotation": 45,
              "gridPosition": "start",
              "gridThickness": 0
            },
          
            "valueAxes": [
          
              {
              "id":"ventas",
              "title": "Bs. Ventas",
              "gridThickness": 0,
              "position": "right",
              "axisColor": ventaColor,
              "axisThickness": 3,
              "axisAlpha": 1,
              "minimum": 0
              },
              {
              "id": "v2",
              "gridThickness": 0,
              "lineColor": "#FF0000",
              "axisColor": "#2694b6",
              "unit": "%",
              "position": "left",
              "title": "% Cumplimiento de Cuota",
              "axisThickness": 3,
              "axisAlpha": 1,
              "startOnAxis": true,
              "minimum": 0,
              "negativeLineColor": "#637bb6",
              "negativeBase": 100,
              },
              {
                "guides": [ {
                    "valueAxis": "v2",
                    "lineColor": "#2694b6", 
                    "value": 100,
                    "label": "100%",
                    "inside": true,
                    "position": "left",
                    "dashLength": 5
                  } ]
              }, 
          
            
          ],
          
            "graphs": [ 
              {
                "id": "v1",
                "title": "Venta",
                "valueField": "monto_total",
                "lineColor": ventaColor,
                "balloonText": "[[title]]: [[value]] Bs.F",
                "type": "column",
                "lineAlpha": 0.1,
                "fillAlphas": 1,
                "labelText": " ",
                "labelPosition": "inside",
                "color": "#fff",
                "labelFunction": function(item) {
                    /**
                     * Calculate total of values across all
                     * columns in the graph
                     */
                     var total = 0;
                     for(var i = 0; i < config.dataProvider.length; i++) {
                       total += config.dataProvider[i][item.graph.valueField];
                     }
                    
                    /**
                     * Calculate percet value of this label
                     */
                     var percent = Math.round( ( item.values.value / total ) * 1000 ) / 10;
                     return percent + "%";
                  }
              },
              {
                "title": "Cuota",
                "valueField": "cuota_total",
                "lineColor": cuotaColor,
                "balloonText": "[[title]]: [[value]] Bs.F",
                "fillAlphas": 1,
                "type": "column",
                "clustered":false,
                "columnWidth":0.5,
              },    
               {
              "valueAxis": "v2",
              "valueField": "cumplimiento",
              "title": "Cumplimiento",
              "balloonText": "[[title]]: [[value]]%",
              "unit": "%",
              "lineAlpha": 0,
              "type": "smoothedLine",
              "lineColor": "#2694b6",
              "lineThickness": 5,
              "bullet": "round",
              "bulletBorderColor": "#000",
              "bulletColor": "#2694b6",
              "bulletBorderThickness": 1,
              "bulletBorderAlpha": 1,
            } ],
          //   "chartScrollbar": {
          //     "graph": "v2",
          //     "oppositeAxis": false,
          //     "scrollbarHeight": 40,
          //     "backgroundAlpha": 0,
          //     "selectedBackgroundAlpha": 0.1,
          //     "selectedBackgroundColor": "#888888",
          //     "graphFillAlpha": 0,
          //     "graphLineAlpha": 0.5,
          //     "selectedGraphFillAlpha": 0,
          //     "selectedGraphLineAlpha": 1,
          //     "autoGridCount": false,
          //     "offset":80,
          //     "color": "#AAAAAA"
          // },
            "chartCursor": {
              "cursorAlpha": 0,
              "zoomable": true,
              "categoryBalloonEnabled": false
            },
            // "mouseWheelZoomEnabled": true,
            "export": {
              "enabled": true,
            //   "fileName": "Ranking Ventas de Saldo Recargas P2P consultado el " + moment().format('DD/MM/YYYY'),
                  "columnNames": {
                      "direccion__nombre": "Dirección",
                      "gerente__nombre": "Gerente",
                      "empresa__nombre": "Empresa",
                      "distribuidor__nombre": "Sucursal",
                      "monto_total": "Venta",
                      "cuota_total": "Cuota",
                      "cumplimiento": "% Cumplimiento"
                  },
              "menuReviver": function(item,li) {
                if (item.format === "XLSX") {
                  item.name = "Ranking";
                }
                return li;
              }
          
            }
          }

        return (
            <div>
                <AmCharts.React style={{ width: "100%", height: "500px"}} options={config} />
            </div>
           
        )
    }
    }
}

export {Chart}