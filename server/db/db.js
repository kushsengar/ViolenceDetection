import mongoose from 'mongoose';
const connectToDatabase=async()=>{
    try{
        await mongoose.connect("mongodb+srv://anujjsengar:Anuj%40082004@anujjsengar.2ordy.mongodb.net/?retryWrites=true&w=majority&appName=anujjsengar")
        console.log("MongoDB Connected Successfully");
    }
    catch(error){
        console.log("Error in Connecting to MongoDB");
        console.log(error);
    }
}
export default connectToDatabase;