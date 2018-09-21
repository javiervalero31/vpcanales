Vue.component("panel", {
  delimiters: ['[[', ']]'],
  template:`
  <div class="row">
    <div class="panel-default col-md-11">
       <div class="panel-heading">

       <h1><slot name="titulo"></slot></h1>
       <div class="btn-group pull-right">
           <slot name="seleccionador"></slot>
       </div>
       <span class="clearfix"></span>

       </div>
       <div class="panel panel-body">
         <div class="row">
           <div class="col-md-4">
             <label><slot name="label1"></slot></label>
             <slot name="filtro1"></slot>
           </div>
           <div class="col-md-4">
             <label><slot name="label2"></slot></label>
             <slot name="filtro2"></slot>
           </div>
           <div class="col-md-4">
             <label><slot name="label3"></slot></label>
             <slot name="filtro3"></slot>
           </div>
         </div>
         <div class="row">
           <div class="col-md-4">
             <label><slot name="label4"></slot></label>
             <slot name="filtro4"></slot>
           </div>
           <div class="col-md-4">
             <label><slot name="label5"></slot></label>
             <slot name="filtro5"></slot>
           </div>
           <div class="col-md-4">
             <label><slot name="label6"></slot></label>
             <slot name="filtro6"></slot>
           </div>
         </div>
         <div class="row">
           <div class="col-md-10 col-md-offset-1">
             <hr>
             <slot name="grafico"></slot>
           </div>
         </div>
       </div>
    </div>

  </div>
  `
})
