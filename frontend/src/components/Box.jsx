import React, { Component } from 'react'

export default class Box extends Component {
    render() {
        return (
            <div className={'box box-' + this.props.color}>
                <div className="box-header with-border">
                    <h3 className="box-title">{this.props.title}</h3>
                    <div className="box-tools pull-right">
                        {/* <!-- Buttons, labels, and many other things can be placed here! --> */}
                        {/* <!-- Here is a label for example --> */}
                        {(this.props.label)? 
                            <span className={'label label-' + this.props.color} >{this.props.label}</span>
                            :
                            null
                        }
                        <button type="button" className="btn btn-box-tool" data-widget="collapse">
                            <i className="fa fa-minus" title="Minimizar"></i>
                        </button>
                        <button type="button" className="btn btn-box-tool" id="btnFiltroRecargasP2PGerente" title="Filtro">
                            <i className="fa fa-filter"></i>
                        </button>
                        <button type="button" className="btn btn-box-tool" data-widget="remove" title="Cerrar">
                            <i className="fa fa-times"></i>
                        </button>
                    </div>
                    {/* <!-- /.box-tools --> */}
                </div>
                {/* <!-- /.box-header --> */}
                <div className="box-body">
                    {/* The body of the box */}
                    {this.props.children}
                </div>
                {/* <!-- /.box-body --> */}
                <div className="box-footer">
                    {/* The footer of the box */}
                </div>    
            </div>
        )
    }
}
