import React, { Component } from 'react'

export default class NavBar extends Component {
    render() {
        const pages = ['home', 'ranking', 'about']
        let navList = pages.map( (page, i) =>
            page === 'home' ? 
            <a href='/recargas/' key={'page-' + i}>{page} </a> 
            : <a  href={'/recargas/' + page } key={'page-' + i} >{page} </a> 
            )

        return (
            <div>
            {navList}        
            </div>
        )
    }
}
