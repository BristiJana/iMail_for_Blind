import React, { useCallback, useState ,useEffect} from 'react'
import { useHistory } from 'react-router-dom';
import { Controlled as ControlledZoom } from 'react-medium-image-zoom'
import 'react-medium-image-zoom/dist/styles.css'
import ReactAudioPlayer from 'react-audio-player'
import './App.css';



var fix={
  color:'green',
  width:'400px',
  height:'400px'
};
function App() {


  const [isZoomed, setIsZoomed] = useState(false)
const [isLoaded, setIsLoaded] = useState(false);
const history = useHistory();

  const handleImgLoad = useCallback(() => {
    setIsZoomed(true)
  }, [])

  const handleZoomChange = useCallback(shouldZoom => {
    setIsZoomed(shouldZoom)
    
  }, [])

useEffect(() => {
  const timer = setTimeout(() => {
    history.push('/main');
    window.location.reload(false);
  }, 4200);
  
}, []);
  

       
    
  return (
    <div>
    <audio controls autoplay>
  <source src="https://mixkit.co/free-sound-effects/bell/" type="audio/ogg"/>
  
</audio>
    <ControlledZoom isZoomed={isZoomed} onZoomChange={handleZoomChange}>

      <img
        alt="that wanaka tree"
        onLoad={handleImgLoad}
        src="https://content.presentermedia.com/content/animsp/00014000/14063/letter_open_up_blank_card_300_wht.gif"
        width="100%"
      />
    </ControlledZoom></div>
  );}



export default App;
