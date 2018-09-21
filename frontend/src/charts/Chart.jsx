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
            this.setState({dataProvider: data.ventas_por_fecha, loading: false})
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
            "type": "serial",
            "titles":[{"text":"Act. Diaria"}],
            "dataDateFormat": "YYYY-MM-DD",
            "language": "es",
            "decimalSeparator": ",",
            "thousandsSeparator": ".",
            "valueAxes": [
                {
                    "axisTitleOffset": 12,
                    "axisAlpha": 0.21,
                    "axisColor": "#8E8E8E",
                    "fontSize": 10,
                    "gridColor": "#FFFFFF",
                    "tickLength": 0,
                    "title": "Bs. Ventas"
                }
            ],
            "categoryField": "tiempo__fecha",
            "categoryAxis": {
                "dashLength": 1,
                "minorGridEnabled": false,
                "titleRotation": 0,
                "titleColor": "#000000",
                "autoRotateAngle": 0,
                "gridPosition": "start",
                "gridCount": 60,
                "startOnAxis": true ,
                "axisAlpha": 0.16,
                "axisColor": "#555555",
                "fillColor": "#555555",
                "fontSize": 10,
                "gridColor": "#FFFFFF",
                "gridThickness": 0,
                "tickPosition": "start",
                "tickLength": 20,
                "labelOffset": -9,
                "labelRotation": 57.6,
                "parseDates": true,
                "labelFunction": function(valueText, date, categoryAxis) {
                    return date.toLocaleDateString();
                  },
                "dataDateFormat": [
                    {period:'DD',format:'DD'},
                    {period:'WW',format:'DD MMM'},
                    {period:'MM',format:'MMM'},
                    {period:'YYYY',format:'YYYY'}],
                "equalSpacing": true,
            },
            "graphs": [
                {
                    "id": "monto_id",
                    "title": "Venta",
                    "valueField": "monto_total",
                    "type": "smoothedLine",
                    "balloonText": "[[title]]: [[value]] Bs.F",
                    "balloonColor": ventaColor,
                    "bullet": "round",
                    "bulletBorderThickness": 1,
                    "bulletSize": 3,
                    "cursorBulletAlpha": 0,
                    "lineColor": ventaColor,
                    "fillAlphas": 1,
                    // "fillAlphas": 1,
                    // "fixedColumnWidth": 0.2,
                    // "fixedColumnWidth": 10.2,
                    "gapPeriod": 10,
                    "lineAlpha": 0.81,
                    "topRadius": 0,
                },
                {
                    "id": "cuota_id",
                    "valueField": "cuota_total",
                    "type": "column",
                    
                    // "type": "column",
                    "balloonText": "[[title]]: [[value]] Bs.F",
                    "title": "Cuota",
                    "animationPlayed": true,
                    "bullet": "round",
                    "bulletSize": 3,
                    // "fillAlphas": 0.14,
                    "fillAlphas": 0.55,
                    "lineAlpha": 0.75,
                    "lineColor": cuotaColor,
                    "negativeFillAlphas": 0,
                    "negativeLineAlpha": 0,
                    "negativeLineColor": "#000000",
                    "topRadius": 0,
                },
                {
                    "id": "AmGraph-5",
                    "title": "Cumplimiento (%)",
                    "unit": '%',
                    "valueField": "porcentaje_cumplimiento",
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
                    "type": "none"
                }
            ],
            // "mouseWheelZoomEnabled": true,
            "chartCursor": {
                "enabled": true,
                // 'pan':true,
                "valueLineEnabled": true,
                "valueLineAlpha": 0.2,
                "animationDuration": 0.22,
                "categoryBalloonAlpha": 0.61,
                "categoryBalloonDateFormat": "MMM DD",
                "cursorPosition": "mouse",
                "cursorAlpha": 0.05,
                "fullWidth": true,
                "graphBulletAlpha": 0,
                "leaveAfterTouch": false,
                // "selectWithoutZooming": true,
                "zoomable": true,
                "categoryBalloonFunction": function(date) {
                    return date.toLocaleDateString();
                }
            },
            "chartScrollbar": {
                "graph": "monto_id",
                "oppositeAxis": false,
                "scrollbarHeight": 40,
                "backgroundAlpha": 0,
                "selectedBackgroundAlpha": 0.1,
                "selectedBackgroundColor": "#888888",
                "graphFillAlpha": 0,
                "graphLineAlpha": 0.5,
                "selectedGraphFillAlpha": 0,
                "selectedGraphLineAlpha": 1,
                "autoGridCount": false,
                "offset":80,
                "color": "#AAAAAA"
            },
            //   "columnWidth": 0,
            "autoMarginOffset": 23,
            "marginTop": 40,
            "marginRight": 40,
            "marginBottom": 0,
            "marginLeft": 0,
            "plotAreaBorderColor": "#888888",
            "color": "#544e4e",
            // "mouseWheelZoomEnabled": true,
            "sequencedAnimation": false,
            "fontSize": 13,
            "theme": "light",
            "touchClickDuration": 1,
            "trendLines": [],
            "guides": [],
            "allLabels": [],
            "balloon": {
                "borderThickness": 1,
                "showBullet": true
            },
            "legend": {
                "enabled": true,
                "align": "center",
                "bottom": 0,
                "color": "#544e4e",
                "equalWidths": false,
                "fontSize": 12,
                "labelText": "[[title]]:",
                "right": 0,
                "rollOverColor": "#6D6D6D",
                "spacing": 60,
                "switchType": "v",
                "top": 0,
                "valueAlign": "left",
                "verticalGap": 10
            },
            
            "dataProvider": this.state.dataProvider,
            "export": {
                "enabled": true,
                "fileName": "Recargas Totales",
                "columnNames": {
                    "tiempo__fecha": "Fecha",
                    "monto_total": "Venta",
                    "cuota_total": "Cuota",
                    "porcentaje_cumplimiento": "% Cumplimiento",
                },
                "menuReviver": function(item,li) {
                    if (item.format === "XLSX") {
                      item.name = "Act. Diaria.";
                    }
                    return li;
                }
            }
        } //End graph   


        return (
            <div>
                <AmCharts.React style={{ width: "100%", height: "500px"}} options={config} />
            </div>
           
        )
    }
    }
}

export {Chart}