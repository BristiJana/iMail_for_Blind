import React, { Suspense, useCallback, useState ,useEffect, useMemo} from 'react'
import { useHistory } from 'react-router-dom';
import { Canvas } from "react-three-fiber";
import Hello from "./Hello.js";
import "./App.css";
 
 
 
function Main() {

const box = {
    color: 'black',
    textDecoration:'none'
}
const fea={

  borderRadius:'40%',
   width:'120px',
   height:'120px',
   marginLeft:'40px',
   marginRight:'50px'
}

const threed={

  marginTop:'40px',
  borderRadius:'100%',
  height:'340px',


}
const uc={
  marginLeft:'20px',
  marginTop:'20px',
textAlign:'center',
paddingTop:'20px'

}
const exfe={

  marginTop:'100px',
  
}
const fi={

  fontSize: '40px',
  color: 'white'
}
const [value, setValue] = useState('')
 

  const changeHandler = value => {
    setValue(value)
  }

       
    
  return (
    <div className="top">


<div class="wrapper">
       
        <nav id="sidebar">
            <div class="sidebar-header">
                <h3><img  style={fea} src="https://www.freeiconspng.com/thumbs/gmail-icon/gmail-logo-icon-2.png"/>
                </h3>
            </div>

            <ul class="list-unstyled components ps-0 mb-1" style={exfe}>
            
                    
      
      
        <a class="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse" data-bs-target="#orders-collapse" aria-expanded="false">
         <center><b style={fi}>iMAIL</b></center>
        </a>
        <div class="collapse" id="orders-collapse">
        <center>
          {/* <p>
          Lorem Ipsum is simply dummy text of the printing and typesetting industry.
          Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer
          took a galley of type and scrambled it to make a type specimen book.
          It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
          It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
          and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
          </p> */}
          </center>
        </div>
      
            </ul>

            
        </nav>

        
        <div id="content">

            
<div className="ub" >
            
<center>
            <div className="row">

 <div className="col-lg-12 introclass">
 <div  style={box}>
<div class="card mb-3 unc"style={{height:'300px'}} >
  <div class="row g-0">
    
    <div class="col-md-8">
      <div class="card-body">
        <h5 class="card-title" style={uc}>About this Project</h5>
        <p class="card-text">The revolution of Internet has transformed several areas of our world to make life of people simple as they now have access to all the information they want. It has altered the way people communicate with one another. E-Mail has become the most dependable way of communication over Internet for sending or receiving some important data, whether it is for business, education or for academic use. But to access the features of Email, one should be able to see the screen and access it using mouse and keyboard. In spite of the advancements in technologies, E-Mail still remains useless for people with vision impairments. 
iMail is a speech based mailing system for visually impaired. The user will be able to operate all functionality of Gmail, the most prominent emailing system used around the world, using voice command only. This web application uses text-to-speech and speech-to-text module to make Gmail accessible for users with visual impairments. Unlike existing systems which focuses more on Graphical User Interface friendliness of normal user, this system focuses on providing accessibility to blind people. </p>

      </div>
    </div>
  </div>
</div>
</div>
</div>

<div className="col-lg-12 introclass">
 
      <img style={threed}src="https://media.giphy.com/media/26u4cqVR8dsmedTJ6/giphy.gif"/>
    </div>
  




</div>

</center>
  </div></div>
  



</div>
       </div>




  );}



export default Main;
