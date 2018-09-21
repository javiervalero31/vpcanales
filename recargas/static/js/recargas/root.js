let app = new Vue({
    el:"#root",
    delimiters: ['[[',']]'],
    data:{
        msg: "Direcciones!!!",
        lider: false,
        directions: [],
        bootDates: [],
        dropDownActive: false,
        showModal: false,
        itemSelected: ''
    },
    methods:{
        isActive() {
            this.dropDownActive = !this.dropDownActive
        }
    }
    ,
    created () {
        
        fetch('/recargas/api/filtros/')
        .then( response => response.json())
        .then( json => {
            console.log(json)
            this.lider = json.results[0].filtro
        });
        
        fetch('/recargas/api/P2P/recargas_resumen/')
        .then( response => response.json())
        .then( json => {
            // console.log(json)
            this.directions = json.direcciones  
            this.bootDates = json.bounds
        });

        

    }
})