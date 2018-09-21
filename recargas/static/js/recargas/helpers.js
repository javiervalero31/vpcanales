//set filters when 'Total' is hitted.
let lastManager;
let lastLeaders = [];

function filterSet(expression, queryUrl = '/recargas/api/P2P/recargas_resumen/'){
    switch(expression) {
        case 1:
            console.log('filterSet case 1');
            console.log(queryUrl);
            $.ajax({
                method: "GET",
                url: queryUrl,
                success: function(response) {
                    console.log('Promise resolve');
                    console.log('Updating filters:');

                    // TODO: Refact this to a function
                    for( let i = 0; i < response.direcciones.length; i ++){
                        // if (response.por_direccion[i].direccion__nombre == 'DESJERARQUIZADO'){continue}
                        $('#direccionFilter').append($("<option value='&direccion__nombre=" + response.direcciones[i].nombre + "' >" + response.direcciones[i].nombre + "</option>"))
                    }

                    for( let i = 0; i< response.part_region.length; i++){
                        $('#regionFilter').append($("<option value='&region__nombre=" + response.part_region[i].region__nombre + "' >" + response.part_region[i].region__nombre + "</option>"))
                    }
                    
                    for( let i = 0; i < response.gerentes.length; i++){
                        // if (response.gerentes[i].gerente__nombre == 'DESJERARQUIZADO'){continue}
                        $('#gerenteFilter').append($("<option value='&gerente__nombre=" + response.gerentes[i].nombre + "' >" + response.gerentes[i].nombre + "</option>"))
                    
                    
                    for( let i=0; i< response.lideres.length; i++){
                        // if (response.gerentes[i].gerente__nombre == 'DESJERARQUIZADO'){continue}
                        if(response.lideres[i].activo){
                            $('#liderFilter')
                            .append($("<option value='&lider__nombre=" + 
                                response.lideres[i].nombre + "' >" + 
                                response.lideres[i].nombre + "</option>")
                            )
                        } else {
                            $('#liderFilter')
                            .append($("<option value='&lider__nombre=" + 
                                response.lideres[i].nombre + "' >" + 
                                response.lideres[i].nombre  + "</option>")
                            )
                        }
                    }

                    
                    }
                    for( var i = 0; i < response.distribuidores_agrupados.length; i++){
                        // if (response.distribuidores_agrupados[i].empresa__nombre == 'DESJERARQUIZADO'){continue}
                        if (response.distribuidores_agrupados[i].activo){
                            $('#empresaFilter')
                            .append($("<option value='&empresa__nombre=" + 
                                response.distribuidores_agrupados[i].nombre + "' >" + 
                                response.distribuidores_agrupados[i].nombre + "</option>")
                            )
                        } else {
                            $('#empresaFilter')
                            .append($("<option value='&empresa__nombre=" + 
                                response.distribuidores_agrupados[i].nombre + "' >" + 
                                response.distribuidores_agrupados[i].nombre + "</option>")
                                .addClass('inactivo')
                            )
                        }
                    }
                    
                    for( var i = 0; i < response.distribuidores.length; i++){
                        if ( (i > 0 && response.distribuidores[i - 1].zona != response.distribuidores[i].zona && response.distribuidores[i].activo) || (i == 0 && response.distribuidores[i].activo) ){
                            $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.distribuidores[i].zona + "' >" + response.distribuidores[i].zona + "</option>"))
                        } else {
                            $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.distribuidores[i].zona + "' >" + response.distribuidores[i].zona + "</option>"))
                        }
                    }
                    console.log('Filters updated.');
                    console.log('updating charts');
                    
                    chart.dataProvider = response.ventas_por_fecha;
                    chart.validateData();
                    chart.animateAgain();
                    updateTotalchart(response);
                    
                    console.log('charts updated')
                    console.log('_end')
                    
                    // Feature change to bars
                    // if (response.precision == 'month'){
                        //     chart.dataProvider = response.ventas_por_fecha;
                        //     console.log(chart.type);
                        //     chart.graphs[0].type = 'smoothedLine';
                        //     chart.graphs[1].type = 'smoothedLine';
                        // updateTotalchart(response);
                        //     chart.validateNow();
                        //     chart.validateData();
                        //     console.log(chart.type);
                        // } else {
                    //     chart.dataProvider = response.ventas_por_fecha;
                    //     chart.graphs[0].type = 'column';
                    //     chart.graphs[1].type = 'column';
                    //     // column
                    //     chart.validateNow();
                    // }
                    // totalChart.dataProvider = response.totales;
                    // totalChart.validateNow();
                    // totalChart.validateData();
                }
            })
        break;
        default:
            //Init date for charts /// TODO: MONTH FINISH
            // var inicio = "tiempo__fecha__gte=" + moment('2018-06-01').startOf('month').format('YYYY-MM-DD')
            // var fin = "tiempo__fecha__lte=" + moment('2018-06-30').format('YYYY-MM-DD')
            if (moment().month() === moment().subtract(1,'month').endOf('month')){
                console.log('====================================');
                console.log('');
                console.log('====================================');
            }
            // var inicio = "tiempo__fecha__gte=" + moment('2018-07-01').startOf('month').format('YYYY-MM-DD')
            // var fin = "tiempo__fecha__lte=" + moment('2018-07-01').endOf('month').format('YYYY-MM-DD')
            var inicio = "tiempo__fecha__gte=" + moment().startOf('month').format('YYYY-MM-DD')
            var fin = "tiempo__fecha__lte=" + moment().subtract(1,'day').format('YYYY-MM-DD')
            console.log('Inicio', inicio);
            
            console.log('Fin', fin);
            
            let todayUrl = baseQuery() + inicio + '&' + fin;
            
            $.ajax({
                method: "GET",
                url:  todayUrl,
                success: function(response) {
                    // TODO: Refact this to a function
                    for( let i = 0; i < response.direcciones.length; i++){
                        $('#direccionFilter')
                        .append($("<option value='&direccion__nombre=" + 
                            response.direcciones[i].nombre + "' >" + 
                            response.direcciones[i].nombre + "</option>")
                        )
                    }

                    for( let i = 0; i< response.part_region.length; i++){
                        $('#regionFilter')
                        .append(
                            $("<option value='&region__nombre=" + 
                            response.part_region[i].region__nombre + "' >" + 
                            response.part_region[i].region__nombre + "</option>")
                        )
                    }

                    for( let i = 0; i < response.gerentes.length; i++){
                        if( response.gerentes[i].activo){
                            $('#gerenteFilter')
                            .append(
                                $("<option value='&gerente__nombre=" + 
                                    response.gerentes[i].nombre + "' >" +
                                    response.gerentes[i].nombre + "</option>"
                                )
                            )
                        } else {
                            $('#gerenteFilter')
                            .append(
                                $("<option value='&gerente__nombre=" + 
                                    response.gerentes[i].nombre + "' >" +
                                    response.gerentes[i].nombre + "</option>"
                                ).addClass('inactivo')
                            )
                        }
                    }

                    for( let i=0; i< response.lideres.length; i++){
                        if(response.lideres[i].activo){
                            $('#liderFilter')
                            .append(
                                $("<option value='&lider__nombre=" + 
                            response.lideres[i].nombre + "' >" + 
                                    response.lideres[i].nombre + "</option>")
                                )
                        } else {
                            $('#liderFilter')
                            .append(
                                $("<option value='&lider__nombre=" + 
                            response.lideres[i].nombre + "' >" + 
                                    response.lideres[i].nombre + "</option>")
                                .addClass('inactivo')
                            )
                        }
                    }

                    for( var i = 0; i < response.distribuidores_agrupados.length; i++){
                        if(response.distribuidores_agrupados[i].activo){
                            $('#empresaFilter')
                            .append(
                                $("<option value='&empresa__nombre=" + 
                                response.distribuidores_agrupados[i].nombre + "' >" + 
                                response.distribuidores_agrupados[i].nombre + "</option>")
                            )
                        } else {
                            $('#empresaFilter')
                            .append(
                                $("<option value='&empresa__nombre=" + 
                                response.distribuidores_agrupados[i].nombre + "' >" + 
                                response.distribuidores_agrupados[i].nombre + "</option>")
                                .addClass('inactivo')
                            )
                        }
                    }
        
                    for( var i = 0; i < response.distribuidores.length; i++){
                        if ( (i > 0 && response.distribuidores[i - 1].zona != response.distribuidores[i].zona && response.distribuidores[i].activo) || (i == 0 && response.distribuidores[i].activo) ){
                        $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.distribuidores[i].zona + "' >" + response.distribuidores[i].zona + "</option>"))
                        // console.log('El distribuidor ' + response.distribuidores[i].zona + ' esta activo');
                        } else {
                        console.log('Nombre de Sucursal Repetida')
                        // $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.distribuidores[i].zona + "' >" + response.distribuidores[i].zona + "</option>"))
                        // console.log('El distribuidor ' + response.distribuidores[i].vd_code + ' esta activo');
                        }
                    }

                    // Get initial data for graphs
                    chart.dataProvider = response.ventas_por_fecha;
                    chart.validateData();
                    updateTotalchart(response)
                    rankingP2P.dataProvider = response.part_direction;
                    rankingP2P.validateData();
                    // empresaP2P.dataProvider = response.part_company;
                    // empresaP2P.validateData();
                    // const max_fecha_db = moment(response.bounds.max_time);
                    // const min_fecha_db = moment(response.bounds.min_time);
                    // $('#dataDate').text('Datos actualizados hasta el ' + max_fecha_db.format('dddd') + ' ' + max_fecha_db.format('DD') + ' de ' + max_fecha_db.format('MMMM')  + ' de ' + max_fecha_db.format('YYYY') + '.')
                    // console.log(max_fecha_db.startOf('month'));
                    // console.log('filterSet default response '+ todayUrl);
                    // console.log(response.totales);
                    // response.ventas_por_fecha.forEach(function (element){
                    //     console.log(moment(element.tiempo__fecha).format('DD/MM/YYYY'));
                    // });
                    const maxFechaDB = moment(response.real_up_to.tiempo__fecha);
                    $('#dataDate').text('Data actualizada hasta el ' + maxFechaDB.format('DD') + ' de ' + maxFechaDB.format('MMMM')  + ' de ' + maxFechaDB.format('YYYY') + '.')


                   

                    // $('input[name="datefilter"]').filter('#ventas-saldo').daterangepicker({
                       
                    //     startDate: moment().startOf('month'),  
                    //     endDate:  moment(maxFechaDB),
                    //     minDate: moment('2017-08-01'),
                    //     maxDate: moment(maxFechaDB), 
                
                    //     autoUpdateInput: true,
                    //     locale: {
                    //         cancelLabel: 'Cancelar',
                    //         applyLabel: 'Filtrar',
                    //         fromLabel: 'Desde',
                    //         toLabel: 'Hasta',
                    //         customRangeLabel: 'Personalizado'
                    //     },
                    //     ranges:{
                    //         'Todo': [moment('2017-08-01'), moment(maxFechaDB)],
                    //         // 'Mes Actual': [moment('2018-06-01').startOf('month'), moment('2018-06-30')],  //TODO: Change this.
                    //         'Mes Actual': [moment(maxFechaDB).startOf('month'), moment(maxFechaDB)], 
                    //         'Ultimo Mes Cerrado': [moment(maxFechaDB).subtract(1, 'month').startOf('month'), moment(maxFechaDB).subtract(1,'month').endOf('month')]
                    //     }
                        
                    // });


                        console.log('Elegimos Todo.');
                } // endSuccess
            }) //endAjax
            
    }
}


// this should return an array of filters
function getFilters(){
  return null
}
// *************** CLEAN

// selective clear of filters passend in.
function clearSelectFilter(){
    for ( var i = 0; i < arguments.length; i++){
        $(arguments[i])
            .find('option')
            .remove()
            .end()
            .append('<option value="">Total</option>')
            .val('')
        ;
        // console.log("se borro " + arguments[i]);
    }
}

function clearAllFilters(){
    clearSelectFilter('#direccionFilter', '#regionFilter', '#gerenteFilter', '#liderFilter', '#empresaFilter', '#distribuidorFilter')
}

// GATERING

function dimNameActiveUrl(dimName, ActiveStatus) {
    if (ActiveStatus == '')
        return
    if (dimName == 'Distribuidor') {
        dimName = 'Empresa'
    } else if ( dimName == 'Sucursal'){
        dimName = 'Distribuidor'
    }

    return '&' + dimName.toLowerCase() + '__activo=' + ActiveStatus
}

function updateChartData(queryUrl) {
    $.ajax({
        method: "GET",
        url: queryUrl,
        success: function(response) {
            chart.dataProvider = response.ventas_por_fecha;
            chart.validateData();
            totalChart.dataProvider = response.totales;
            totalChart.validateNow();
            totalChart.validateData();
            updateTotalchart(response);
        }
    })
}

function updateTotalchart(response){
    let results = [];
    results.push(response.totales)

    let pickerDataVentasSaldo = $('#ventas-saldo').data('daterangepicker')
    console.log(pickerDataVentasSaldo);
    let currentMonth = pickerDataVentasSaldo.endDate.month() === moment().month() && pickerDataVentasSaldo.startDate.month() === moment().month();
    let currentYear = pickerDataVentasSaldo.endDate.year() == moment().year() && pickerDataVentasSaldo.startDate.year() === moment().year();
    let matchCurrentDate = currentMonth && currentYear

    let pickerLabelVentasSaldo = pickerDataVentasSaldo.chosenLabel
    if (matchCurrentDate || pickerLabelVentasSaldo == 'Mes Actual' || pickerLabelVentasSaldo == undefined){
        delete response.probable_cierre.total_venta
        delete response.probable_cierre.total_cuota
        delete response.probable_cierre.cumplimiento
        response.probable_cierre.total_venta = response.probable_cierre.pc
        response.probable_cierre.additional = "(probable)"
        response.probable_cierre.dashLengthColumn = 5
        response.probable_cierre.alpha = 0.2
        response.probable_cierre.total = 'Cierre Probable'
        response.probable_cierre.total_cuota = Math.round(response.probable_cierre.cuota_mes)
        // response.probable_cierre.cumplimiento = response.probable_cierre.cumplimiento * 100
        response.probable_cierre.cumplimiento =  Math.round((response.probable_cierre.pc / response.probable_cierre.cuota_mes) * 1000) / 10
        results.push(response.probable_cierre)
        console.log('Probable Cierre', response.probable_cierre)
        console.log('Ventas saldo Daterangepicker', $('#ventas-saldo').data('daterangepicker'));
    }
    

    totalChart.dataProvider = results;
    console.log('data Provider total Chart', results);
    totalChart.dataProvider[0].total = 'Real';
    if( totalChart.dataProvider[0].total == undefined ){
        console.log('totalChart is undefined!')
        
        var totalObj = {total: 'Acum.'};
        console.log(totalChart.dataProvider[0])

    }
    
    // totalChart.dataProvider[0].cumplimiento += '%';
    totalChart.validateNow();
    totalChart.validateData();
    totalChart.animateAgain();
}
// These operations are computed on every filter

function getTimeRangeFilter(){
    const startDate = $('input[name="datefilter"]').data('daterangepicker').startDate.format('YYYY-MM-DD')
    const endDate = $('input[name="datefilter"]').data('daterangepicker').endDate.format('YYYY-MM-DD')
    return 'tiempo__fecha__gte='.concat(startDate) + '&' + 'tiempo__fecha__lte='.concat(endDate)
}

function getFiltersState(filters){
    const state = [];
    state.push(filters);
    return state.join("") // the & are appended by default on option value prop.
}

function baseQuery(){
    return '/recargas/api/P2P/recargas_resumen/?'
}

function composeUrl(){
    return baseQuery() + getTimeRangeFilter() 
}

//***  fill filters with the rigth data 
function fillFilters(response, array, key, element) {
    arreglo = array
    llave = key
    string_llave = `'&${llave}=`  
    for( let i = 0; i < response.arreglo.length; i++){
        if ( response.arreglo.length ==1 ){
            $(element)
            .append(
                "<option selected value="+ string_llave + 
                    response.arreglo[i].llave + "' >" + 
                    response.arreglo[i].llave + 
                "</option>"
            )
        }
    }
}

function fillFiltersByDimension(queryUrl, otherDimensions){
    $.ajax({
        method: 'GET',
        url: queryUrl, 
        success: function (response){
            
            fillFilters(response, )
    
        }
    })
}
// *** fillers ***
//*** TODO: refactorize to a succinct method => fillFiltersByDimension
function fillFiltersByDirection(queryUrl){
    $.ajax({
        method: 'GET',
        url: queryUrl, 
        success: function (response){
            for( var i = 0; i < response.por_gerente.length; i++){
                $('#gerenteFilter')
                .append(
                    $("<option value='&gerente__nombre=" + response.por_gerente[i].gerente__nombre + "' >" + response.por_gerente[i].gerente__nombre + "</option>"))
            }
            
            for( let i = 0; i < response.part_leader.length; i++){
                $('#liderFilter').append($("<option value='&lider__nombre=" + response.part_leader[i].lider__nombre + "' >" + response.part_leader[i].lider__nombre + "</option>"))
            }

            for( let i = 0; i < response.part_region.length; i++){
                $('#regionFilter').append($("<option value='&region__nombre=" + response.part_region[i].region__nombre + "' >" + response.part_region[i].region__nombre + "</option>"))
            }
            
            for( var i = 0; i < response.por_empresa.length; i++){
                if(  $("#empresaFilter option:selected").text() != response.por_empresa[0].empresa__nombre ){
                    //This should never happen.
                    $('#empresaFilter').append($("<option value='&empresa__nombre=" + response.por_empresa[i].empresa__nombre + "' >" + response.por_empresa[i].empresa__nombre + "</option>"))
                } 
            }

            for( var i = 0; i < response.distribuidor_por_direccion.length; i++){
                $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.distribuidor_por_direccion[i].nombre + "' >" + response.distribuidor_por_direccion[i].nombre  + "</option>"))
            }
            console.log('filtros actualizados por direccion.');
        }
    })
}

function fillFiltersByRegion(queryUrl){
    $.ajax({
        method: 'GET',
        url: queryUrl,
        success: function(response){
            console.log('====================================');
            console.log($('#direccionFilter').children());
            console.log('====================================');
            for (let i = 0; i < response.part_direction.length; i++){
                if (response.part_direction.length == 1 ){
                    clearSelectFilter('#direccionFilter')
                    $('#direccionFilter')
                    .append(
                        $("<option selected value='&direccion__nombre=" + response.part_direction[i].direccion__nombre + " '>" + 
                        response.part_direction[i].direccion__nombre + "</option>")
                    )
                } else {
                    console.log('NOT')
                }
            }
           


            for( var i = 0; i < response.por_gerente.length; i++){
                $('#gerenteFilter')
                .append(
                    $("<option selected value='&gerente__nombre=" + response.por_gerente[i].gerente__nombre + "' >" +
                     response.por_gerente[i].gerente__nombre + "</option>")
                )
            }
            
            for( let i = 0; i < response.part_leader.length; i++){
                $('#liderFilter')
                .append(
                    $("<option value=&'lider__nombre=" + response.part_leader[i].lider__nombre + "' >" + 
                        response.part_leader[i].lider__nombre + "</option>")
                )
            }

            for( var i = 0; i < response.por_empresa.length; i++){
                if(  $("#empresaFilter option:selected").text() != response.por_empresa[0].empresa__nombre ){
                    $('#empresaFilter').append($("<option value='&empresa__nombre=" + response.por_empresa[i].empresa__nombre + "' >" + response.por_empresa[i].empresa__nombre + "</option>"))
                } 
            }

            for( var i = 0; i < response.distribuidor_por_direccion.length; i++){
                $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.distribuidor_por_direccion[i].nombre + "' >" + response.distribuidor_por_direccion[i].nombre  + "</option>"))
            }
        }
    })
}

function fillFiltersByManager(queryUrl){
    $.ajax({
        method: 'GET',
        url: queryUrl, 
        success: function (response){
            for( var i = 0; i < response.por_direccion.length; i ++){
                // if (response.por_direccion[i].direccion__nombre == 'DESJERARQUIZADO'){
                //     continue
                // } 

                // if (response.por_direccion.length == 1){
                //     $('#direccionFilter option').eq().attr('selected','selected')
                //     console.log(
                //         $('#direccionFilter option').filter(response.por_direccion[0].direccion__nombre),
                //         $('#direccionFilter option:selected').text()
                //     );
                // }

                $('#direccionFilter')
                .append(
                    $("<option selected value='&direccion__nombre=" + 
                    response.por_direccion[i].direccion__nombre + "' >" + 
                    response.por_direccion[i].direccion__nombre + "</option>")
                )
            }

            for( let i = 0; i < response.part_region.length; i++){
                if (response.part_region.length == 1) {
                    $('#regionFilter')
                    .append(
                        $("<option selected value='&region__nombre=" +
                        response.part_region[i].region__nombre + "' >" +
                        response.part_region[i].region__nombre + "</option>")
                    )
                } else {
                    $('#regionFilter')
                    .append(
                        $("<option value='&region__nombre=" +
                        response.part_region[i].region__nombre + "' >" +
                        response.part_region[i].region__nombre + "</option>")
                    )
                }


                
            }
            clearSelectFilter('#liderFilter')
            for( let i = 0; i < response.part_leader.length; i++){
                $('#liderFilter').append($("<option value=&lider__nombre=" + response.part_leader[i].lider__nombre + ">" + response.part_leader[i].lider__nombre + "</option>"))
            }

            
          
            for( var i = 0; i < response.por_empresa.length; i++){
                // if (response.por_empresa[i].empresa__nombre == 'DESJERARQUIZADO'){continue}
                if ( response.por_empresa.length == 1){
                    $('#empresaFilter').append($("<option selected value='&empresa__nombre=" + response.por_empresa[i].empresa__nombre + "' >" + response.por_empresa[i].empresa__nombre + "</option>"))
                    
                }else{
                    $('#empresaFilter').append($("<option value='&empresa__nombre=" + response.por_empresa[i].empresa__nombre + "' >" + response.por_empresa[i].empresa__nombre + "</option>"))

                }
            }
            for( var i = 0; i < response.por_distribuidor.length; i++){
                // if (response.por_distribuidor[i].distribuidor__zona == 'DESJERARQUIZADO'){continue}
                if( response.por_distribuidor.length == 1) {
                    $('#distribuidorFilter').append($("<option selected value='&distribuidor__zona=" + response.por_distribuidor[i].distribuidor__zona + "' >" + response.por_distribuidor[i].distribuidor__zona  + "</option>"))
                } else {
                    $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.por_distribuidor[i].distribuidor__zona + "' >" + response.por_distribuidor[i].distribuidor__zona  + "</option>"))
                    
                }
            }               
            console.log('filtros actualizados por gerente.');
        }
    })
}

function fillFiltersByLeader(queryUrl){
    $.ajax({
        method: 'GET',
        url: queryUrl, 
        success: function (response){
            for( var i = 0; i < response.por_direccion.length; i ++){
                $('#direccionFilter')
                .append(
                    $("<option selected value='&direccion__nombre=" + 
                    response.por_direccion[i].direccion__nombre + "' >" + 
                    response.por_direccion[i].direccion__nombre + "</option>")
                )
            }

            
                if (response.part_region.length == 1) {
                    clearSelectFilter('#regionFilter')
                    $('#regionFilter')
                    .append(
                        $("<option selected value='&region__nombre=" +
                        response.part_region[0].region__nombre + "' >" +
                        response.part_region[0].region__nombre + "</option>")
                    )
                } else {
                    clearSelectFilter('#regionFilter')
                    
                    for( let i = 0; i < response.part_region.length; i++){
                        $('#regionFilter')
                        .append(
                            $("<option value='&region__nombre=" +
                            response.part_region[i].region__nombre + "' >" +
                            response.part_region[i].region__nombre + "</option>")
                        )
                    }
                }

            for( var i = 0; i < response.por_gerente.length; i++){
                if (response.por_gerente.length == 1){
                    clearSelectFilter('#gerenteFilter')
                    $('#gerenteFilter').append($("<option selected value='&gerente__nombre=" + response.por_gerente[i].gerente__nombre + "' >" + response.por_gerente[i].gerente__nombre + "</option>"))
                    lastManager = response.por_gerente[i].gerente__nombre
                } else {
                    clearSelectFilter('#gerenteFilter') 
                    $('#gerenteFilter').append($("<option value='&gerente__nombre=" + response.por_gerente[i].gerente__nombre + "' >" + response.por_gerente[i].gerente__nombre + "</option>"))

                }
            }

            for( var i = 0; i < response.por_empresa.length; i++){
                // if (response.por_empresa[i].empresa__nombre == 'DESJERARQUIZADO'){continue}
                if ( response.por_empresa.length == 1){
                    $('#empresaFilter').append($("<option selected value='&empresa__nombre=" + response.por_empresa[i].empresa__nombre + "' >" + response.por_empresa[i].empresa__nombre + "</option>"))
                    
                }else{
                    $('#empresaFilter').append($("<option value='&empresa__nombre=" + response.por_empresa[i].empresa__nombre + "' >" + response.por_empresa[i].empresa__nombre + "</option>"))

                }
            }

            for( var i = 0; i < response.por_distribuidor.length; i++){
                // if (response.por_distribuidor[i].distribuidor__zona == 'DESJERARQUIZADO'){continue}
                if( response.por_distribuidor.length == 1) {
                    $('#distribuidorFilter').append($("<option selected value='&distribuidor__zona=" + response.por_distribuidor[i].distribuidor__zona + "' >" + response.por_distribuidor[i].distribuidor__zona  + "</option>"))
                } else {
                    $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.por_distribuidor[i].distribuidor__zona + "' >" + response.por_distribuidor[i].distribuidor__zona  + "</option>"))
                    
                }
            }       


        }
    })
    console.log('Filtros actualizados por lider.')
}
function fillFilterByCompany(queryUrl){
    $.ajax({
        method: 'GET',
        url: queryUrl, 
        success: function (response){
            console.log('Direction length: ' + response.por_direccion.length)
            for( var i = 0; i < response.por_direccion.length; i ++){
                if ( response.por_direccion.length == 1){
                    if(  $("#direccionFilter option:selected").text() != response.por_direccion[0].direccion__nombre ){
                        //This should never happen.
                        $('#direccionFilter').append($("<option selected value='&direccion__nombre=" + response.por_direccion[i].direccion__nombre + "' >" + response.por_direccion[i].direccion__nombre + "</option>"))
                    }
                    // console.log('en el filtro texto: ' + $("#direccionFilter option:selected").text());
                    // console.log('ajax response: ' + response.por_direccion[0].direccion__nombre);
                } else {
                    console.log("DOUG!");
                    $('#direccionFilter').append($("<option value='&direccion__nombre=" + response.por_direccion[i].direccion__nombre + "' >" + response.por_direccion[i].direccion__nombre + "</option>"))
                }
            }
            
            for( let i = 0; i < response.part_region.length; i++){
                if(response.part_region.length == 1) {

                    $('#regionFilter').append($("<option selected value='&region__nombre=" + response.part_region[i].region__nombre + "' >" + response.part_region[i].region__nombre + "</option>"))
                } else {

                    $('#regionFilter').append($("<option value='&region__nombre=" + response.part_region[i].region__nombre + "' >" + response.part_region[i].region__nombre + "</option>"))
                }
            }

            clearSelectFilter('#gerenteFilter')
            for( var i = 0; i < response.por_gerente.length; i++){
                console.log('Doing nothing for now in gerentes.');
                if (response.por_gerente.length == 1){
                    $('#gerenteFilter').append($("<option selected value='&gerente__nombre=" + response.por_gerente[i].gerente__nombre + "' >" + response.por_gerente[i].gerente__nombre + "</option>"))
                    
                } else {
                    $('#gerenteFilter').append($("<option value='&gerente__nombre=" + response.por_gerente[i].gerente__nombre + "' >" + response.por_gerente[i].gerente__nombre + "</option>"))

                }
            }
            
            if ( response.part_leader.length == 1){
                clearSelectFilter('#liderFilter')
                $('#liderFilter')
                .append(
                    $("<option selected value=&'lider__nombre=" + 
                    response.part_leader[0].lider__nombre + "' >" + 
                    response.part_leader[0].lider__nombre + "</option>")
                )
            } else {
                clearSelectFilter('#liderFilter')
                for( let i = 0; i < response.part_leader.length; i++){

                    $('#liderFilter')
                    .append(
                        $("<option value=&'lider__nombre=" + response.part_leader[i].lider__nombre + "' >" + 
                        response.part_leader[i].lider__nombre + "</option>")
                    )
                }
            }
            
            if (response.por_distribuidor.length == 1){
                clearSelectFilter('#distribuidorFilter')
                console.log('paso ' + response.por_distribuidor[0].distribuidor__zona);
                $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.por_distribuidor[0].distribuidor__zona + "' >" + response.por_distribuidor[0].distribuidor__zona  + "</option>"))             
                $('#distribuidorFilter option').eq(1).attr('selected','selected')
                console.log(
                    $('#distribuidorFilter option').eq(1).text()
                );
            } 
            if (response.por_distribuidor.length > 1){
                clearSelectFilter('#distribuidorFilter')

                for( var i = 0; i < response.por_distribuidor.length; i++){
                        $('#distribuidorFilter').append($("<option value='&distribuidor__zona=" + response.por_distribuidor[i].distribuidor__zona + "' >" + response.por_distribuidor[i].distribuidor__zona  + "</option>"))
                }
            }



            console.log('filtros actualizados por empresa');
        }
    })
}
// fill the distribuidor
function fillFiltersByDistribuitor(queryUrl, manager){
    $.ajax({
        method: 'GET',
        url: queryUrl,
        success: function (response){
            console.log('Success: ', manager);
            

            clearSelectFilter('#direccionFilter')
            for( var i = 0; i < response.por_direccion.length; i ++){
                $('#direccionFilter').append($("<option selected value='&direccion__nombre=" + response.por_direccion[i].direccion__nombre + "' >" + response.por_direccion[i].direccion__nombre + "</option>"))
            }

            for( var i = 0; i < response.part_region.length; i++){
                if (response.part_region.length == 1){
                    clearSelectFilter('#regionFilter')
                    $('#regionFilter')
                    .append(
                        $("<option selected value='&region__nombre=" + 
                            response.part_region[i].region__nombre + "' >" + 
                            response.part_region[i].region__nombre + 
                          "</option>"
                        )
                    )
                } else if ( response.part_region[i].region__nombre == manager){
                    console.log('CARESTE ESTE /D-A')
                } else {
                    // console.log("It's something missing?");
                    clearSelectFilter('#regionFilter')
                    $('#regionFilter')
                    .append(
                        $("<option value='&region__nombre=" + 
                            response.part_region[i].region__nombre + "' >" + 
                            response.part_region[i].region__nombre + 
                          "</option>"
                        )
                    )
                }
            }

            for( var i = 0; i < response.por_gerente.length; i++){
                if (response.por_gerente.length == 1){
                    clearSelectFilter('#gerenteFilter')
                    $('#gerenteFilter')
                    .append(
                        $("<option selected value='&gerente__nombre=" + 
                            response.por_gerente[i].gerente__nombre + "' >" + 
                            response.por_gerente[i].gerente__nombre + 
                          "</option>"
                        )
                    )
                } else if ( response.por_gerente[i].gerente__nombre == manager){
                    console.log('CARESTE ESTE /D-A')
                } else {
                    // console.log("It's something missing?");
                    $('#gerenteFilter')
                    .append(
                        $("<option value='&gerente__nombre=" + 
                            response.por_gerente[i].gerente__nombre + "' >" + 
                            response.por_gerente[i].gerente__nombre + 
                          "</option>"
                        )
                    )
                }
            }

            if ( response.part_leader.length == 1){
                clearSelectFilter('#liderFilter')
                $('#liderFilter')
                .append(
                    $("<option selected value=&'lider__nombre=" + 
                    response.part_leader[0].lider__nombre + "' >" + 
                    response.part_leader[0].lider__nombre + "</option>")
                )
            } else {
                clearSelectFilter('#liderFilter')
                for( let i = 0; i < response.part_leader.length; i++){
                    $('#liderFilter')
                    .append(
                        $("<option value=&'lider__nombre=" + response.part_leader[i].lider__nombre + "' >" + 
                        response.part_leader[i].lider__nombre + "</option>")
                    )
                }
            }
                
            if (response.por_empresa.length == 1) {
                
                clearSelectFilter('#empresaFilter')
                $('#empresaFilter')
                .append(
                    $("<option selected value='&empresa__nombre=" + 
                        response.por_empresa[0].empresa__nombre + "' >" + 
                        response.por_empresa[0].empresa__nombre  + 
                        "</option>"
                    )
                )
            } else {
                for( var i = 0; i < response.por_empresa.length; i++){
                    console.log('estado de el filtro empresa: ', $('#empresaFilter'));
                    clearSelectFilter('#empresaFilter')
                    console.log('Borrado');
                    
                    $('#empresaFilter')
                    .append(
                        $("<option value='&empresa__nombre=" + 
                            response.por_empresa[i].empresa__nombre + "' >" + 
                            response.por_empresa[i].empresa__nombre  + 
                            "</option>"
                        )
                    )
                }
            }
           
            console.log('filtros actualizados por distribuidor'); 
        }
    })
}


