var empresaP2P = AmCharts.makeChart( "chart-by-dim-2", {
    "theme": "light",
    "language": "es",
    "decimalSeparator": ",",
    "thousandsSeparator": ".",
    "type": "serial",
    "dataProvider": [],
    "categoryField": "empresa__nombre",
    "depth3D": 20,
    "angle": 30,
  
    "categoryAxis": {
      "labelRotation": 45,
      "gridPosition": "start"
    },
  
    "valueAxes": [ {
      "title": "Bs. Ventas"
    }
    ,{
      "id": "v2",
      "unit": "%",
      "position": "right",
      "title": "% Cumplimiento de Cuota",
    } ],
  
    "graphs": [ {
      "valueField": "monto_total",
      "colorField": cuotaColor,
      "lineColor": ventaColor,
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
        for(var i = 0; i < empresaP2P.dataProvider.length; i++) {
          total += empresaP2P.dataProvider[i][item.graph.valueField];
        }
        
        /**
         * Calculate percet value of this label
         */
        var percent = Math.round( ( item.values.value / total ) * 1000 ) / 10;
        return percent + "%";
      },
    }, {
      "lineAlpha": 0.9,
      "title": "",
      "type": "smoothedLine",
      "lineColor": cuotaColor,
      "lineThickness": 3,
      "bullet": "round",
      "bulletBorderColor": "#fff",
      "bulletBorderThickness": 2,
      "bulletBorderAlpha": 1,
      "valueField": "cumplimiento",
      "valueAxis": "v2"
    } ],
  
    "chartCursor": {
      "cursorAlpha": 0,
      "zoomable": false,
      "categoryBalloonEnabled": false
    },
  
    "export": {
      "enabled": true,
      "fileName": "Recargas por gerentes " + moment().format('DD/MM/YYYY'),
          "columnNames": {
              "gerente__nombre": "Gerente",
              "monto_total": "Venta",
              "cuota_total": "Cuota",
              "cumplimiento": "% Cumplimiento"
          }
    }
  } );