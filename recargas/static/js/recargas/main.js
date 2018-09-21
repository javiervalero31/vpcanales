var ventasSaldoStartDate;
var ventasSaldoEndDate;

$(function() {
    //Filters 
    let filtersIds = ['#direccionFilter', '#regionFilter', '#gerenteFilter','#liderFilter', '#empresaFilter', '#distribuidorFilter']
 
    //toggle filters
    $('#btnFiltroRecargasP2P').on('click', function(){
        $('#p2p-filter').toggle()
    })

    $('#btnFiltroRecargasP2PGerente').on('click', function(){
        $('#filtroRecargasP2PGerente').toggle()
    })

    $('#visualizarInactivos').on('click', function(){
        if ($(this).text() == 'Sí') {
            $(this).text('No')
        } else {
            $(this).text('Sí')
        }
        $('.inactivo').toggle()
    })

    //change the dim graph attributes
    // TODO: put this on a function
    //ranking
    $('#p2p-dim-selector').on('change', 'input', function() {
        let rangoFecha = $('input[name="datefilter"]').filter('#ranking').data('daterangepicker')
        let selection = $('input[name=options]:checked', '#p2p-dim-selector').filter('.dimensions').val();
        let selectionVisibility = $('input[name=visuals]:checked').val(); // true, false, null
        urlDimRanking = dimNameActiveUrl(selection, selectionVisibility)
        let originalText = $('label:checked').text()
        
        if( rangoFecha != undefined){
            range = "tiempo__fecha__gte=" + rangoFecha.startDate.format('YYYY-MM-DD') + 
            "&tiempo__fecha__lte=" + rangoFecha.endDate.format('YYYY-MM-DD');
            var queryUrl = baseQuery() + range
        } else {
            range = "tiempo__fecha__gte=" + moment().startOf('month').format('YYYY-MM-DD') + 
            "&tiempo__fecha__lte=" + moment().subtract(1,'day').format('YYYY-MM-DD');
            var queryUrl = baseQuery() + range
        }
        
        if( urlDimRanking != undefined ) {
            queryUrl += urlDimRanking
        }
          
        console.log(queryUrl);
        $.ajax({
            method: "GET",
            url: queryUrl,
            success: function(response) {
                if(selection == 'Direccion')
                {
                    rankingP2P.categoryField="direccion__nombre"
                    rankingP2P.dataProvider = response.part_direction;
                    rankingP2P.validateData();
                    rankingP2P.animateAgain();
                }
                else if (selection == 'Region'){
                    rankingP2P.categoryField="region__nombre"
                    rankingP2P.dataProvider = response.part_region;
                    rankingP2P.validateData();
                    rankingP2P.animateAgain();
                }
                else if (selection == 'Gerente'){
                    rankingP2P.categoryField="gerente__nombre"
                    rankingP2P.dataProvider = response.total_gerentes;
                    rankingP2P.validateData();
                    rankingP2P.animateAgain();
                }else if (selection == 'Lider'){
                    rankingP2P.categoryField="lider__nombre"
                    rankingP2P.dataProvider = response.part_leader;
                    rankingP2P.validateData();
                    rankingP2P.animateAgain();
                }
                else if (selection == 'Distribuidor'){
                    rankingP2P.categoryField="empresa__nombre"
                    rankingP2P.dataProvider = response.part_company;
                    rankingP2P.validateData();
                    rankingP2P.animateAgain();
                } 
                else {
                    rankingP2P.categoryField="distribuidor__zona"
                    rankingP2P.dataProvider = response.part_distribuitor;
                    rankingP2P.validateData();
                    rankingP2P.animateAgain();
                }
            }
        })

    });
   
    // filter for direction
    $('select[id="direccionFilter"]').change( function () {
        queryUrl = composeUrl() + $("select option:selected").attr('value')
        console.log(queryUrl)
        empresaFilterState = $("#empresaFilter option:selected").text()
        directionFilterState = $("#direccionFilter option:selected").text()
        regionFilsterState = $("#regionFilter option:selected").text()

        if ( directionFilterState !== 'Total' && empresaFilterState !== 'Total' ){
            queryUrl += '&empresa__nombre=' + empresaFilterState
            clearSelectFilter("#gerenteFilter","#distribuidorFilter")
            fillFiltersByDirection(queryUrl)
            console.log("AGAIN");
            console.log(queryUrl);
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        } else if( directionFilterState !== 'Total' ) {
            clearSelectFilter('#regionFilter','#gerenteFilter','#liderFilter', '#empresaFilter', '#distribuidorFilter')
            console.log('La direccion no es Total queryUrl: ', queryUrl)
            fillFiltersByDirection(queryUrl)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        } else {
            clearAllFilters()
            filterSet(1, queryUrl)
        }
    })


    $('select[id="regionFilter"').change( function(){
        queryUrl = composeUrl() + $("#regionFilter option:selected").attr('value')
        console.log(queryUrl);
        if ($("#regionFilter option:selected").text() !== 'Total' && $('#direccionFilter option:selected').text() == 'Total' ){
            let regionFilter = filtersIds
            // borrados = regionFilter.splice(filtersIds.indexOf('#direccionFilter'), 2)
            console.log('regionFilter: ', regionFilter);
            // clearSelectFilter(...regionFilter)
            clearSelectFilter('#gerenteFilter','#liderFilter', '#empresaFilter', '#distribuidorFilter')
            fillFiltersByRegion(queryUrl)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        } else if ( $("#regionFilter option:selected").text() !== 'Total' && $('#direccionFilter option:selected').text() !== 'Total' ) {
            clearSelectFilter('#gerenteFilter','#liderFilter', '#empresaFilter', '#distribuidorFilter')
            fillFiltersByRegion(queryUrl)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        } 
        else {
            clearAllFilters()
            filterSet(1, queryUrl)
        }
    })

    $('select[id="gerenteFilter"]').change( function () {
        // var direccionFiltro = $("select option:selected").attr('value') //Show if direccion is !== 'Total'
        let gerenteFilter = $("#gerenteFilter option:selected")
        queryUrl = composeUrl() + gerenteFilter.attr('value')
        console.log(queryUrl);
        if (gerenteFilter.text() !== 'Total'){
            clearSelectFilter('#direccionFilter', '#regionFilter', '#liderFilter', '#empresaFilter', '#distribuidorFilter')
            fillFiltersByManager(queryUrl)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        } else {
            clearAllFilters()
            filterSet(1, queryUrl)
        }
    })

    $('select[id="liderFilter"]').change( function () {
        // var direccionFiltro = $("select option:selected").attr('value') //Show if direccion is !== 'Total'
        console.log(lastManager);
        console.log(lastLeaders);
        let gerenteFilter = $("#gerenteFilter option:selected")
        let regionFilter = $("#regionFilter option:selected")
        let liderFilter = $("#liderFilter option:selected")
        // queryUrl = composeUrl() + liderFilter.attr('value')
        queryUrl = composeUrl() + '&lider__nombre=' + liderFilter.text()
        console.log(queryUrl);
        if (liderFilter.text() != 'Total' && gerenteFilter.text() == 'Total' ){
            clearSelectFilter('#direccionFilter', '#regionFilter', '#gerenteFilter', '#empresaFilter', '#distribuidorFilter')
            console.log('AQUI');
            console.log(queryUrl);
            fillFiltersByLeader(queryUrl)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        } else if( gerenteFilter.text() !== 'Total' && liderFilter.text() != 'Total' ) {
            clearSelectFilter('#direccionFilter','#empresaFilter','#distribuidorFilter')
            // queryUrl += '&region__nombre=' + regionFilter.text()
            // queryUrl += '&gerente__nombre=' + gerenteFilter.text()
            console.log('ALLA');
            console.log(queryUrl);
            fillFiltersByLeader(queryUrl)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        } else {
            console.log('NINGUNO');
            queryUrl = composeUrl()
            clearAllFilters()
            filterSet(1, queryUrl)
        }
    })

    $('select[id="empresaFilter"]').change( function (){
        let empresaSelected = $('#empresaFilter option:selected')
        let gerenteSelected = $('#gerenteFilter option:selected')
       
        let direccionSelected = $('#direccionFilter option:selected')

        queryUrl = composeUrl() + empresaSelected.attr('value')
        //reset filters if 'Total'
        if ( empresaSelected.text() == 'Total'){
            console.log("La empresa es Total, se borran todos los filtros.");
            clearAllFilters()
            console.log('El filtro por empresa va a consultar: ',queryUrl);
            filterSet(1, queryUrl)
            console.log('La Promesa enviada y resolviendose, fin cambio en el filtro.');
            
        } else {
            
            if (gerenteSelected.text() !== 'Total'){
                // var filterState = [];
                // filterState.push($('#direccionFilter').val(), $('#gerenteFilter').val());
                // queryUrl += filterState.join("");
                
                // console.log(gerenteSelectedCopy);
                // if (gerenteSelectedCopy !== gerenteSelected ){
                //     queryUrl += '&gerente__nombre=' + gerenteSelected.text()
                // }
                
                
                // console.log(gerenteSelectedCopy);
                clearSelectFilter('#direccionFilter', '#regionFilter', '#gerenteFilter', '#distribuidorFilter')
            } else {
                console.log('La empresa no es Total y el gerente tampoco');
                clearSelectFilter('#direccionFilter', '#regionFilter', '#gerenteFilter', '#distribuidorFilter')
            }

            console.log('endpoint a consultar: ' + queryUrl);
            
            fillFilterByCompany(queryUrl)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        }
    })

    $('select[id="distribuidorFilter"]').change( function (){
        // queryUrl += $('#distribuidorFilter option:selected').attr('value')
        let regionSelected = $('#regionFilter option:selected')
        let gerenteSelected = $('#gerenteFilter option:selected')
        let distribuidorSelected = $("#distribuidorFilter option:selected")
        let empresaSelected = $("#empresaFilter option:selected")
        // let liderSelected = $('#liderFilter option:selected')

        queryUrl = composeUrl() + distribuidorSelected.attr('value')
        console.log(queryUrl);
        
        if ( distribuidorSelected.text() !== 'Total' && empresaSelected.text() !== 'Total' ){
                console.log('empresa: ' + empresaSelected.text())
                // queryUrl += '&empresa__nombre=' + empresaSelected.text()
                clearSelectFilter('#direccionFilter', '#gerenteFilter')
                console.log('la empresa ha sido seleccionada');
                
                if (gerenteSelected.text() !== 'Total') {
                    var gerenteFilterState = $('#gerenteFilter option:selected').text()
                    // console.log(gerenteFilterState);
                    // console.log(gerenteSelected.text());
                // if (liderSelected.text() !== 'Total') {
                //     queryUrl += '&lider__nombre=' + liderSelected.text()
                // }

            } else {
                console.log('la empresa no fue seleccionada');
                clearSelectFilter('#direccionFilter', '#gerenteFilter')
            }
            fillFiltersByDistribuitor(queryUrl, gerenteFilterState)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        } else if (distribuidorSelected.text() == 'Total') {
            clearAllFilters()
            filterSet(1, queryUrl)
        } else {
            clearSelectFilter('#direccionFilter', '#regionFilter', '#gerenteFilter','#liderFilter', '#empresaFilter')
            fillFiltersByDistribuitor(queryUrl)
            updateChartData(queryUrl)
            updateTotalchart(queryUrl)
        }
        console.log('fin');
    })

    // daterangepicker config
    $('input[name="datefilter"]').daterangepicker({
        // startDate: moment('2018-07-01').startOf('month'),  //TODO: Change this.
        // endDate:  moment('2018-07-31'),  //TODO: Change this.
        startDate: moment().startOf('month'),  
        endDate:  moment().subtract(1,'day'),
        minDate: moment('2017-08-01'),
        maxDate: moment().subtract(1,'day'), 

        autoUpdateInput: true,
        locale: {
            cancelLabel: 'Cancelar',
            applyLabel: 'Filtrar',
            fromLabel: 'Desde',
            toLabel: 'Hasta',
            customRangeLabel: 'Personalizado'
        },
        ranges:{
            'Todo': [moment('2017-08-01'), moment().subtract(1,'day')],
            // 'Mes Actual': [moment('2018-06-01').startOf('month'), moment('2018-06-30')],  //TODO: Change this.
            'Mes Actual': [moment().startOf('month'), moment().subtract(1,'day')], 
            'Ultimo Mes Cerrado': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1,'month').endOf('month')]
        }
        
    });
    
    $('input[name="datefilter"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });
    
    $('input[name="datefilter"]').filter('#ventas-saldo').on('apply.daterangepicker', function(ev, picker) {
        // $(this).val(picker.startDate.format('L') + ' - ' + picker.endDate.format('L'));`// config autoUpdate dependecy
        var inicio = "tiempo__fecha__gte=" + picker.startDate.format('YYYY-MM-DD');
        var fin = "tiempo__fecha__lte=" + picker.endDate.format('YYYY-MM-DD');
        var rango = inicio + "&" + fin;
        var filterState = [];
        filterState.push($('#direccionFilter').val(), $('#gerenteFilter').val(), $('#regionFilter').val(), $('#empresaFilter').val(), $('#distribuidorFilter').val());
        console.log('Estado del filtro');
        console.log(filterState);
        var baseUrl = '/recargas/api/P2P/recargas_resumen/?'
        var queryUrl = filterState.join("");
        const endpoint = baseUrl + rango + queryUrl;
        console.log(endpoint)
        console.log('Jojoto');
        
        $.ajax({
            method: "GET",
            url: endpoint,
            success: function(response) {
                console.log("Data from time filter:");
                console.log(response.ventas_por_fecha);
                console.log(response.total_gerentes);

                if ($('#empresaFilter').text() != 'Total') {
                    clearSelectFilter('#direccionFilter', '#regionFilter', '#gerenteFilter','#liderFilter')
                    fillFilterByCompany(endpoint) 
                } else {
                    console.log('Actualizar aqui.');
                    
                }

                chart.dataProvider = response.ventas_por_fecha;
                chart.validateData();
                updateTotalchart(response)  
            } //endSuccess
        })// endAjax endpoint
    }); //endApplyDatepicker 

}); // end ready jQuery
