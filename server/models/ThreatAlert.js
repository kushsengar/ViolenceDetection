// models/ThreatAlert.js
import mongoose from 'mongoose';

const ThreatAlertSchema = new mongoose.Schema({
  threat_id: {
    type: Number,
    unique: true,
    required: true
    // Auto-increment can be handled by plugins if needed
  },
  image_url: {
    type: String,
    default: null
  },
  latitude: {
    type: Number,
    default: null
  },
  longitude: {
    type: Number,
    default: null
  },
  address: {
    type: String,
    default: null
  },
  timestamp: {
    type: Date,
    default: Date.now
  }
});

// Model creation
const ThreatAlert = mongoose.model('ThreatAlert', ThreatAlertSchema);

export default ThreatAlert;
