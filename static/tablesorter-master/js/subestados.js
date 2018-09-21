 google.load("visualization", "1.1", {
  packages: ["bar", "corechart", "line"]
});

$(function(){
  /* Initial settings */
  var $table = $('table').trigger('chartData');
    $chart = $('#chart'),
    $bar = $('#chartbar'),
    $rowType = $('[name=getrows]'),
    $icons = $('#chart-container i'),
    initType = 'line', // graph types ('pie', 'pie3D', 'line', 'area', 'vbar', 'vstack', 'hbar' or 'hstack')
    chartTitle = '',
    axisTitle = 'Sub-Estado',
    width = 1100,
    height = 600,
    // extra data processing
    processor = function(data) {
       //console.log(data);
      return data;
    },

  // don't change anything below, unless you want to remove some types; modify styles and/or font-awesome icons
  types = {
    pie3D  : { in3D: true,  maxCol: 2, stack: false, type: 'pie',  titleStyle: { color: '#333' }, icon: 'fa-cube' },
    pie    : { in3D: false, maxCol: 2, stack: false, type: 'pie',  titleStyle: { color: '#333' }, icon: 'fa-pie-chart' },
    line   : { in3D: false, maxCol: 99,stack: false, type: 'line', titleStyle: { color: '#333' }, icon: 'fa-line-chart' },
    area   : { in3D: false, maxCol: 5, stack: false, type: 'area', titleStyle: { color: '#333' }, icon: 'fa-area-chart' },
    vbar   : { in3D: false, maxCol: 5, stack: false, type: 'vbar', titleStyle: { color: '#333' }, icon: 'fa-bar-chart' },
    vstack : { in3D: false, maxCol: 5, stack: true,  type: 'vbar', titleStyle: { color: '#333' }, icon: 'fa-tasks fa-rotate-90' },
    hbar   : { in3D: false, maxCol: 5, stack: false, type: 'hbar', titleStyle: { color: '#333' }, icon: 'fa-align-left' },
    hstack : { in3D: false, maxCol: 5, stack: true,  type: 'hbar', titleStyle: { color: '#333' }, icon: 'fa-tasks fa-rotate-180' }
  },
  /* internal variables */
  settings = {
    table : $table,
    chart : $chart[0],
    chartTitle : chartTitle,
    axisTitle : axisTitle,
    type : initType,
    processor : processor
  },
  drawChart = function() {
    if (!$table[0].config) { return; }
    var options, chart, numofcols, data,
      s = settings,
      t = types[s.type],
      obj = s.chart,
      rawdata = $table[0].config.chart.data;
    if ( $.isFunction( s.processor ) ) {
      rawdata = s.processor( rawdata );
    }
    if ( rawdata.length < 2 ) {
      return;
    }
    data = google.visualization.arrayToDataTable( rawdata );

    numofcols = rawdata[1].length;
    if (numofcols > t.maxCol+10) {
      // default to line chart if too many columns selected
      t = types['line'];
    }

    options = {
      title: s.chartTitle,
      chart: {
        title: s.chartTitle
      },
      hAxis: {
        title: s.axisTitle,
        titleTextStyle: t.titleStyle
      },
      vAxis: {},
      is3D: t.in3D,
      isStacked: t.stack,
      width: width,
      height: height
    };

    if (t.type == 'vbar' && !t.stack) {
      chart = new google.charts.Bar(obj);
    } else if (t.type == 'vbar') {
      chart = new google.visualization.ColumnChart(obj);
    } else if (t.type == 'hbar') {
      options.hAxis = {};
      options.vAxis = {
        title: s.axisTitle,
        titleTextStyle: t.titleStyle,
        minValue: 0
      };
      chart = new google.visualization.BarChart(obj);
    } else if (t.type == 'area') {
      chart = new google.visualization.AreaChart(obj);
    } else if (t.type == 'line') {
      chart = new google.charts.Line(obj);
    } else {
      chart = new google.visualization.PieChart(obj);
    }
    chart.draw(data, options);
  };

  $('#chartSelect').change(function() {
    $('#chart-container').slideToggle( $(this).is(':checked') );
    drawChart();
  });

  $icons.click(function(e) {
    if ( $(e.target).hasClass('disabled') ) {
      return true;
    }
    $icons.removeClass('active');
    var $t = $(this).addClass('active');
    $.each(types, function(i, v){
      if ($t.hasClass(v.icon)) {
        settings.type = i;
      }
    });
    drawChart();
  });

  $rowType.on('change', function(){
    $table[0].config.widgetOptions.chart_incRows = $rowType.filter(':checked').attr('data-type');
    // update data, then draw new chart
    $table.trigger('chartData');
    drawChart();
  });

  $table.on('columnUpdate pagerComplete', function(e) {
    var table = this,
      c = table.config,
      t = types['pie'],
      max = t && t.maxCol || 2;
    setTimeout(function() {
      if (table.hasInitialized) {
        $table.trigger('chartData');
        drawChart();
        // update chart icons
        if (typeof c.chart !== 'undefined') {
          var cols =  c.chart.data[0].length;
          if (cols > max) {
            $bar.find('.fa-cube, .fa-pie-chart').addClass('disabled');
            if ($bar.find('.fa-cube, .fa-pie-chart').hasClass('active')) {
              $bar.find('.fa-cube, .fa-pie-chart').removeClass('active');
              $bar.find('.fa-line-chart').addClass('active');
            }
          } else {
            $bar.find('.fa-cube, .fa-pie-chart').removeClass('disabled');
            if (settings.type == 'pie') {
              $bar.find('.active').removeClass('active');
              $bar.find( settings.in3D ? '.fa-cube' : '.fa-pie-chart' ).addClass('active');
            }
          }
        }
      }
    }, 10);
  });

  $table
    .tablesorter({
      showProcessing: true,
      theme: 'grey',
      sortList: [[0, 0]],
          widgets: ['pager', 'zebra', 'filter', 'cssStickyHeaders', 'columnSelector', 'chart'],
      widgetOptions: {
        columnSelector_container: '#columnSelector',
        cssStickyHeaders_filteredToTop: true,
        pager_selectors: { container: '#pager' },
        pager_output: 'Mostrando {startRow} a {endRow} de {filteredRows} resultados',
        pager_size: 1,
        chart_incRows: 'f',
        chart_useSelector: true,

      }


    });

});

