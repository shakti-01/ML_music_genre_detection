import React, { useState,useRef, useEffect } from 'react'

function Home() {
  const [file, setFile] = useState(null);
  const [rec,setRec] = useState(false);
  const result_genre = useRef();
  useEffect(() => {
    result_genre.current.innerText = "Please select a file to upload";
  });
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (file == null) {
      alert('Please select a file to upload');
      return;
    }
    const data = new FormData();
    data.append('audio-file', file);
    result_genre.current.innerText = "PLEASE WAIT ... MODEL IS PROCESSING";
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data
    });
    const res = await response.json();
    console.log(res);

    if (!res.success) {
      result_genre.current.innerText = "error...";
      alert("Give valid audio file");
    }
    else {
      result_genre.current.innerText = "This belongs to "+res.genre+"\nthis is predicted with a confidence of "+res.confidence;
      //show recomendations
      let params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,width=0,height=0,left=-1000,top=-1000`;
      if(rec){
        if(res.genre === 'Jazz')window.open("https://youtu.be/cd_YsXGYsbo",'test',params);
        else if(res.genre === 'Blues')window.open("https://youtu.be/myaUdTT6MV8",'test',params);
        else if(res.genre === 'Classical')window.open("https://youtu.be/_4IRMYuE1hI",'test',params);
        else if(res.genre === 'Country')window.open("https://youtu.be/ftoJ6nqTcbg",'test',params);
        else if(res.genre === 'Disco')window.open("https://youtu.be/Gs069dndIYk",'test',params);
        else if(res.genre === 'Hip-hop')window.open("https://youtu.be/PQZhN65vq9E",'test',params);
        else if(res.genre === 'Metal')window.open("https://youtu.be/hTWKbfoikeg",'test',params);
        else if(res.genre === 'Pop')window.open("https://youtu.be/kJQP7kiw5Fk",'test',params);
        else if(res.genre === 'Reggae')window.open("https://youtu.be/z4ScbuTIbgM",'test',params);
        else if(res.genre === 'Rock')window.open("https://youtu.be/15qAby5CzBQ",'test',params);
      }

    }
  }
  const onChange = (e) => {
    if (e.target.files) setFile(e.target.files[0]);
  }
  return (
    <div className='home'>
      <h1>Music genre detection system</h1>
      <hr />
      <div className='home-main'>
        <form onSubmit={handleSubmit} encType='multipart/form-data'>
          <input type='file' onChange={onChange} accept="audio/wav"/>
          <br />
          <button type='submit'>Find genre</button>
        </form>
        <br />
        <div className='result' ref={result_genre}>blank</div>
        <div><label>Do you want recomendations based on the precdiction?</label><input type='checkbox' checked={rec} onChange={e=>{setRec(!rec)}}></input></div>
      <img src="./model-arc.jpeg" alt="pic-model"/>
      </div>
    </div>
  )
}

export default Home
