var ventaColor = '#014266';
var cuotaColor = '#00C0EF';

var chart = AmCharts.makeChart("chartdiv",   
{
    "type": "serial",
    "titles":[{"text":"Act. Diaria"}],
    "dataDateFormat": "YYYY-MM-DD",
    "language": "es",
    "decimalSeparator": ",",
    "thousandsSeparator": ".",
    "startDuration": 1,
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
            "type": "smoothedLine",
            
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
    "mouseWheelZoomEnabled": true,
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
    "color": "#B7B7B7",
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
        "color": "#6D6D6D",
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
    
    "dataProvider": [],
    "export": {
        "enabled": true,
        "menu": [ {
            "class": "export-main",
            "menu": [{
              "label":"Descargar como...",
              "menu": ["JPG","PDF"]
            }, {
              "label":"Guardar como...",
              "menu": ["XLSX"]
            },{
              "label":"Anotar ...",
              "action": "draw",
      
            },{
              "label":"Imprimir"
            }
          ]
          }],
        "fileName": "Recargas Totales",
        "columnNames": {
            "tiempo__fecha": "Fecha",
            "monto_total": "Venta",
            "cuota_total": "Cuota",
            "porcentaje_cumplimiento": "% Cumplimiento",
        },
        "menuReviver": function(item,li) {
            if (item.format == "XLSX") {
              item.name = "Act. Diaria.";
            }
            return li;
        }
    }
} //End graph   
);

var  totalChart = AmCharts.makeChart( "chartdiv2", {
    "titles":[{"id":"total-acum", "text":"Act. Acumulada"}],
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
    "dataProvider": [],
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
        "fontSize": 10,
        "gridColor": "#FFFFFF",
        "tickLength": 0,
      } ],
    
      "graphs": [ {
        "title"   : "Column graph",
        "valueField": "total_venta",
        "alphaField": "alpha",
        "dashLengthField": "dashLengthColumn",
        "lineColor": ventaColor,
        // "labelText": "[[percents]]%",
        "color": "#fff",
        "title": 'Total Ventas:',
        "type": "column",
        "lineAlpha": 0.75,
        "fillAlphas": 0.7,
        "showBalloon": true,
        },{
        "valueField": "total_cuota",
        "alphaField": "alpha",
        "dashLengthField": "dashLengthColumn",
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
        "labelText": "[[percents]]%",
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
} );


    /**
   * Ajuste decimal de un número.
   *
   * @param {String}  tipo  El tipo de ajuste.
   * @param {Number}  valor El numero.
   * @param {Integer} exp   El exponente (el logaritmo 10 del ajuste base).
   * @returns {Number} El valor ajustado.
   */
//   function decimalAdjust(type, value, exp) {
//     // Si el exp no está definido o es cero...
//     if (typeof exp === 'undefined' || +exp === 0) {
//       return Math[type](value);
//     }
//     value = +value;
//     exp = +exp;
//     // Si el valor no es un número o el exp no es un entero...
//     if (isNaN(value) || !(typeof exp === 'number' && exp % 1 === 0)) {
//       return NaN;
//     }
//     // Shift
//     value = value.toString().split('e');
//     value = Math[type](+(value[0] + 'e' + (value[1] ? (+value[1] - exp) : -exp)));
//     // Shift back
//     value = value.toString().split('e');
//     return +(value[0] + 'e' + (value[1] ? (+value[1] + exp) : exp));
//   }

//   // Decimal round
//   if (!Math.round10) {
//     Math.round10 = function(value, exp) {
//       return decimalAdjust('round', value, exp);
//     };
//   }
//   // Decimal floor
//   if (!Math.floor10) {
//     Math.floor10 = function(value, exp) {
//       return decimalAdjust('floor', value, exp);
//     };
//   }
//   // Decimal ceil
//   if (!Math.ceil10) {
//     Math.ceil10 = function(value, exp) {
//       return decimalAdjust('ceil', value, exp);
//     };
//   }


$(function() {
    // set all filters to Total by default
    // $.get( "/recargas/boot_date_p2p/", function( data ) {
    //     console.log('Fecha: ', data);
        
    //   }, "json" );
    filterSet(0);

    // current month start on 0 so, March is 2
   
    var date = new Date();
    var month = date.getMonth();

});

// $( document ).ready(function() {
//     filterSet(0);
//     console.log( "ready!" );
// });