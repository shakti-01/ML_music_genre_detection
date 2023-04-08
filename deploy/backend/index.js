const express = require('express')
const app = express()
const port = 5000

app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "http://localhost:3000");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  next();
});
app.use(express.json())


app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.post('/predict', (req, res) => {
    res.send('this is a hop hop song...')
})
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})