import express from 'express';
import cors from 'cors';
import connectToDatabase from './db/db.js';
import AlertRoute from './routes/AlertRoute.js';
const app = express();
const PORT = 3000;

// Middleware
app.use(cors());

connectToDatabase();

app.use('/api', AlertRoute);


app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
  });