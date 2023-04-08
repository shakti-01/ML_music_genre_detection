import React from 'react'

function Home() {
  return (
    <div className='home'>
        <h1>Music genre detection system</h1>
        <hr/>
        <div className='home-main'>
            <form>
                <input type='file' placeholder='select music'/>
                <br/>
                <button type='submit'>Find genre</button>
            </form>
            <br/>
            <div className='result'>This belongs to hip-hop</div>
        </div>
    </div>
  )
}

export default Home