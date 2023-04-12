import React, { useState } from 'react'

function Home() {
  const [file, setFile] = useState(null);
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
      alert('nice')
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
          <input type='file' onChange={onChange} />
          <br />
          <button type='submit'>Find genre</button>
        </form>
        <br />
        <div className='result'>This belongs to hip-hop</div>
      </div>
    </div>
  )
}

export default Home