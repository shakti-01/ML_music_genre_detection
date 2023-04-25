import React, { useState,useRef, useEffect } from 'react'

function Home() {
  const [file, setFile] = useState(null);
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
      </div>
    </div>
  )
}

export default Home
