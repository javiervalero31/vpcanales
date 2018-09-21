var rankingP2P = AmCharts.makeChart( "chart-by-dim", {
  "theme": "light",
  "language": "es",
  "decimalSeparator": ",",
  "thousandsSeparator": ".",
  "type": "serial",
  "dataProvider": [],
  "startDuration": 0.7,
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
      "title": "% Cumpl. de Cuota",
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
      "title": "Cuota",
      "valueField": "cuota_total",
      "lineColor": cuotaColor,
      "balloonText": "[[title]]: [[value]] Bs.F",
      "fillAlphas": 1,
      "type": "column",
      "clustered":false,  
    },
    {
      "id": "v1",
      "title": "Venta",
      "columnWidth":0.5,
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
          for(var i = 0; i < rankingP2P.dataProvider.length; i++) {
            total += rankingP2P.dataProvider[i][item.graph.valueField];
          }
          
          /**
           * Calculate percet value of this label
           */
          var percent = Math.round( ( item.values.value / total ) * 1000 ) / 10;
          return percent + "%";
        }
    },    
     {
    "id": "v2",
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
    "markerType": "circle",
    "balloonFunction": function rankingPositions(graphDataItem, graph) {
      var value = 'cumplimiento: '; 
      value += graphDataItem.values.value;
      value += '%'
      value += ', # ' + (graphDataItem.index + 1)
      return value 
    }
  }],
  "chartScrollbar": {
    "graph": "v2",
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
  "chartCursor": {
    "cursorAlpha": 0,
    "zoomable": true,
    "categoryBalloonEnabled": false
  },
  "listeners": [{
    "event": "zoomed",
    "method": function(e) {
      var text = " # " + (e.startIndex + 1) + " " + e.startValue;
      // text += " -- " + "# " +(e.endIndex + 1) + " " + e.endValue;
      document.getElementById("selection").innerHTML = text;
    }
  }],
  "mouseWheelZoomEnabled": true,
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
    "fileName": "Ranking Ventas de Saldo Recargas P2P consultado el " + moment().format('DD/MM/YYYY'),
        "columnNames": {
            "direccion__nombre": "Dirección",
            "region__nombre": "Región",
            "gerente__nombre": "Gerente",
            "lider__nombre": "Líder",
            "empresa__nombre": "Distribuidor",
            "distribuidor__zona": "Sucursal",
            "monto_total": "Venta",
            "cuota_total": "Cuota",
            "cumplimiento": "% Cumplimiento"
        },
    "menuReviver": function(item,li) {
      if (item.format == "XLSX") {
        item.name = "Ranking";
      }
      return li;
    }

  }
} );

var selectedDataPoint;
var chartHistMonth;

rankingP2P.addListener("clickGraphItem", function(event) {
  // check if the new chart is created already
  if (undefined == chartHistMonth) {
    // it's not - create it
    chartHistMonth = AmCharts.makeChart("chart-hist-month", {
      "type": "serial",
      "theme": "light",
      "decimalSeparator": ",",
      "thousandsSeparator": ".",
      "autoMargins": true,
      "marginLeft": 30,
      "marginRight": 8,
      "marginTop": 10,
      "marginBottom": 26,
      "titles": [{
        "text": "Data Mensual"
      }],
      "dataProvider": [],
      "startDuration": 0.7,
      "graphs": [{
        "alphaField": "alpha",
        "balloonText": "<span style='font-size:13px;'>[[title]] en el mes [[category]]:<b>[[value]]</b> Bs.F [[additional]]</span>",
        "dashLengthField": "dashLengthColumn",
        "fillAlphas": 1,
        "title": "Venta",
        "type": "column",
        "valueField": "total",
        "lineColor": ventaColor,
      }],
      "categoryField": "month",
      "categoryAxis": {
        "gridPosition": "start",
        "axisAlpha": 0,
        "tickLength": 0
      },
    });
  }
  
  console.log(event)
  console.log(event.item.dataContext);
  

  var text = event.item.category + " (posición: #" + (event.item.index + 1) + ")";
      document.getElementById("clicked").innerHTML = text;

  console.log(event.item.category) // selected item

      // let selection = $('input[name=options]:checked', '#p2p-dim-selector').val();
      // let queryDimension;

      // if(selection == 'Direccion') {
      //   queryDimension="direccion__nombre"
      // } else if (selection == 'Region') {
      //   queryDimension="region__nombre"
      // } else if (selection == 'Gerente') {
      //   queryDimension="gerente__nombre"
      // } else if (selection == 'Lider') {
      //   queryDimension="lider__nombre"
      // } else if (selection == 'Distribuidor') {
      //   queryDimension="empresa__nombre"
      // } else {
      //   queryDimension="distribuidor__zona"
      // }

        // let queryUrl = `/recargas/api/P2P/recargas_resumen/?${queryDimension}=${event.item.category}`;  
        // $.ajax({
        //     method: "GET",
        //     url: queryUrl,
        //     success: function(response) {
        //       chartHistMonth.dataProvider = response.mensuales;
        //        // validate the new data and make the chart animate again
              
        //       chartHistMonth.validateData();
        //       chartHistMonth.animateAgain();
        //     }
        // })  

  if ('object' === typeof event.item.dataContext) {
    console.log(event.item.dataContext,'Hua!!!')
        // reset alpha of the previously set data point
    if (undefined != selectedDataPoint)
      selectedDataPoint.alpha = 0.5;

    // set alpha so we know which one is selected
    selectedDataPoint = event.item;
    selectedDataPoint.alpha = 0.3;
    rankingP2P.validateData();

  }

});
