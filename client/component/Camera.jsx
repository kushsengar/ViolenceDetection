import React, { useEffect, useState, useRef } from "react";
import alertSound from "../src/assets/alert.mp3";

function Camera() {
  const videoRef = useRef(null);
  const audioRef = useRef(null);

  const [response, setResponse] = useState({ violence_detected: null });
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: "user" } })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        const intervalId = setInterval(captureFrame, 3000);
        return () => clearInterval(intervalId);
      })
      .catch((err) => {
        console.error("Error accessing front camera:", err);
        setIsError(true);
        setErrorMessage("Unable to access camera");
      });
  }, []);

  const captureFrame = async () => {
    if (!videoRef.current) return;

    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(videoRef.current, 0, 0);

    const image = canvas.toDataURL("image/jpeg");

    try {
      const res = await fetch("http://localhost:8000/api/process-frame/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image }),
      });

      const data = await res.json();
      setResponse(data);
      setIsError(false);

      if (data.violence_detected) {
        audioRef.current.play().catch(() => {});
      } else {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
    } catch (err) {
      console.error("Error processing frame:", err);
      setIsError(true);
      setErrorMessage("Error processing frame");
    }
  };

  return (
    <div
      style={{
        position: "relative",
        backgroundColor: "#1f2937", // Tailwind's gray-900
        borderRadius: "1rem",
        overflow: "hidden",
        boxShadow: "0 10px 25px rgba(0, 0, 0, 0.3)",
        width: "100%",
        maxWidth: "768px",
        margin: "2rem auto",
      }}
    >
      {isError && (
        <div
          style={{
            position: "absolute",
            top: "12px",
            left: "12px",
            backgroundColor: "#dc2626", // red-600
            color: "white",
            padding: "0.5rem 1rem",
            borderRadius: "0.375rem",
            fontSize: "0.875rem",
            zIndex: 10,
            boxShadow: "0 2px 6px rgba(0, 0, 0, 0.2)",
          }}
        >
          {errorMessage}
        </div>
      )}

      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        style={{
          width: "100%",
          aspectRatio: "16 / 9",
          objectFit: "cover",
          borderTopLeftRadius: "1rem",
          borderTopRightRadius: "1rem",
        }}
      />

      <div
        style={{
          position: "absolute",
          bottom: "20px",
          left: "50%",
          transform: "translateX(-50%)",
          backgroundColor: "rgba(255, 255, 255, 0.8)",
          backdropFilter: "blur(6px)",
          padding: "0.5rem 1rem",
          borderRadius: "9999px",
          display: "flex",
          alignItems: "center",
          gap: "0.5rem",
          boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
        }}
      >
        <span
          style={{
            width: "12px",
            height: "12px",
            borderRadius: "9999px",
            backgroundColor:
              response.violence_detected === null
                ? "#9ca3af" // gray-400
                : response.violence_detected
                ? "#dc2626" // red-600
                : "#22c55e", // green-500
            animation:
              response.violence_detected === true ? "pulse 1.5s infinite" : "none",
          }}
        />
        <span
          style={{
            fontSize: "0.875rem",
            fontWeight: "600",
            color: "#1f2937", // gray-800
          }}
        >
          {response.violence_detected === null
            ? "Loading..."
            : response.violence_detected
            ? "Violence Detected"
            : "No Violence"}
        </span>
      </div>

      <audio ref={audioRef} src={alertSound} preload="auto" style={{ display: "none" }} />

      {/* Pulse animation */}
      <style>
        {`
          @keyframes pulse {
            0%, 100% {
              opacity: 1;
              transform: scale(1);
            }
            50% {
              opacity: 0.5;
              transform: scale(1.3);
            }
          }
        `}
      </style>
    </div>
  );
}

export default Camera;
