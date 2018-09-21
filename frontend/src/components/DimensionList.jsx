import React from 'react'
import {DisplayName} from './DisplayName'
export function DimensionList(props) {
    return (
        <div>
            {props.nombres.map( name => <DisplayName {...name} /> )}
        </div>
    )
} 