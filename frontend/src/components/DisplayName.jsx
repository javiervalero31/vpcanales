import React from 'react'

export const DisplayName = (props) => {
	return (
    <div style={{margin:'1em'}} key={props.id}>
      <img atl="" src="http://placehold.it/75"  />
      {/* <img width="75" src={props.avatar_url} /> */}
      <div style={{display:'inline-block', marginLeft: 10}}>
      	<div style={{fontSize:'1.25em', fontWeight:'bold'}}>{props.nombre}</div>
     	 	<div>{props.id}</div>  
      </div>
      
    </div>
  );
};