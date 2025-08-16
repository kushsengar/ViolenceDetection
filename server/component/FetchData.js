import ThreatAlert from '../models/ThreatAlert.js'

const FetchData = async(req,res)=>{
    console.log("Fetching Threat Data ------>");
    try{
        const threats=await ThreatAlert.find();
        console.log(threats);
        res.status(200).json(threats);
    }
    catch(error){
        res.status(500).json({message: 'Error in Fetching Data'});
    }
};
export default FetchData;