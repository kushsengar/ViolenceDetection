import express from 'express';
import FetchData from '../component/FetchData.js'
const router=express.Router();

const AlertRoute = router.get('/alert-data', FetchData);

export default AlertRoute;