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
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data
    });
    const res = await response.json();
    console.log(res);

    if (!res.success) {
      alert("Give valid audio file");
    }
    else {
      // alert('Your genre is '+res.genre)
      result_genre.current.innerText = "This belongs to "+res.genre;
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
        <div className='result' ref={result_genre}>This belongs to hip-hop</div>
      </div>
    </div>
  )
}

export default Home