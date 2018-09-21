Vue.component("activaciones-cuotas", {
  props: ['arg'],
  delimiters: ['[[', ']]'],
  template: `
	<div id="chartdiv"></div>
	`,

  watch: {
    'arg': {
      handler: function(newVal) {
        this.paint(),
        chart.dataProvider = this.build_json(newVal),
        chart.valueAxes["0"].maximum = this.getMax(chart.dataProvider,'cantidad','cuota') *1.1
        console.log(this.getMax(chart.dataProvider,'cantidad','cuota'))
        chart.validateData()
      },
      deep: true,
    },
  },


  methods: {
    paint: function() {
      chart = AmCharts.makeChart("chartdiv", {

        "type": "serial",
        "export": {
          "enabled": true
        },
        "theme": "light",
        "startDuration": 2,
        "thousandsSeparator": '.',
        "decimalSeparator":',',
        "valueAxes": [
          {
            "autoGridCount":true,
            "minimum":0,
            "maximum":0,
          }
        ],
        "legend": {
          "equalWidths": false,
          "useGraphSettings": true,
          "valueAlign": "left",
          "valueWidth": 120
        },
        "dataProvider": [],

        "graphs": [{
            "alphaField": "alpha",
            "balloonText": "[[value]] Activaciones",
            "dashLengthField": "dashLength",
            "fillAlphas": 1,
            "legendValueText": "[[value]]",
            "title": "Activaciones:",
            "type": "column",
            "valueField": "cantidad",
            "valueAxis": "distanceAxis",
            "lineColor": "#013552",
          },
          {
            "balloonText": "Cuota de [[value]]",
            "bullet": "round",
            "bulletBorderAlpha": 1,
            "useLineColorForBulletBorder": true,
            "bulletColor": "#ffffff",
            "lineColor":"#17BDE6",
            "legendValueText": "[[value]]",
            "title": "Cuota:",
            "fillAlphas": 0,
            "valueField": "cuota",
            "valueAxis": "latitudeAxis",
            "lineThickness":3
          },
          {
            "balloonText": "Cumplimiento de: [[value]]%",
            "bullet": "round",
            "bulletBorderAlpha": 1,
            "useLineColorForBulletBorder": true,
            "bulletColor": "#FFFFFF",
            "legendValueText": "[[value]]%",
            "title": "Cumplimiento:",
            "fillAlphas": 0,
            "valueField": "cumplimiento",
            "valueAxis": "latitudeAxis",
            // "markerType": "triangleUp",
            "type": "none"
          }
        ],
        "chartCursor": {
          "categoryBalloonDateFormat": "DD",
          "cursorAlpha": 0.1,
          "cursorColor": "#000000",
          "fullWidth": true,
          "valueBalloonsEnabled": false,
          "zoomable": false
        },
        "dataDateFormat": "YYYY-MM-DD",
        "categoryField": "fecha",
        "categoryAxis": {
          "dateFormats": [{
            "period": "DD",
            "format": "DD"
          }, {
            "period": "WW",
            "format": "MMM DD"
          }, {
            "period": "MM",
            "format": "MMM"
          }, {
            "period": "YYYY",
            "format": "YYYY"
          }],
          "parseDates": true,
          "autoGridCount": false,
          "axisColor": "#555555",
          "gridAlpha": 0.1,
          "gridColor": "#FFFFFF",
          "gridCount": 50

        },

      });

      return chart

    },

    build_json: function(arg) {
      var yson = '['
      var flag
      var cuota = this.arg.APIData.Cuota
      var activacion = this.arg.APIData.Activacion
      for (var i in cuota) { // iterate over cuota obj
        flag = false
        if (cuota.hasOwnProperty(i)) { // hasOwnProperty is used to filter propertys from the object
          for (var j in activacion) { //inside, iterare over actividad
            if (activacion.hasOwnProperty(j)) { //hasOwnProperty is used to filter propertys from the object
              if (cuota[i].fecha == activacion[j].fecha) { // ask by date
                yson += '{"fecha":"' + cuota[i].fecha + '","cuota":"' + Math.round(cuota[i].cuota) + '","cantidad":"' + activacion[j].cantidad + '","cumplimiento":"' + Math.round((activacion[j].cantidad / cuota[i].cuota) * 100) + '"},'
                flag = true
              }
            }
          }
        }
        if (flag == false) {
          yson += '{"fecha":"' + cuota[i].fecha + '","cuota":"' + cuota[i].cuota + '","cantidad":"0", "cumplimiento":0},'
        }
      }
      yson = yson.substring(0, yson.length - 1);
      yson += ']'
      yson = JSON.parse(yson)
      return yson;
    },

    getMax: function(arr, prop){
      var max;

      for (var i=0 ; i<arr.length ; i++) {
          if (!max || parseInt(arr[i][prop]) > parseInt(max[prop]))
              max1 = arr[i].cantidad;
      }
      return {max}
    },

  }



});
