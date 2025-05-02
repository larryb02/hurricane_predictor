"use client";
import Image from "next/image";
import styles from "./page.module.css";
import { useState } from "react";

export default function Home() {
  const [selectedLocation, setSelectedLocation] = useState("");
  const [date, setDate] = useState("");
  const validLocations = {
    "PA": {"lon": -77.194527, "lat": 41.2033},
    "NY": {"lon": -74.0060, "lat": 40.7128},
    "FL": {"lon": -81.5158, "lat": 27.6648}
  }; // key = location_name, value = (long,lat)

  async function getForecast(location: string, date: string)
  {
    console.log(`Parameters: {loc: ${location}, date: ${date}}`);
    // await fetch('localhost:8000/forecast');
  }
  return (
    <div>
      Hurricane Prediction Tool
      <select
        value={selectedLocation}
        onChange={(e) => setSelectedLocation(e.target.value)}>
        <option value="" disabled>
          Select a location
        </option>
        {Object.entries(validLocations).map(([key, value]) => (
          <option key={key} value={key}>
            {key}
          </option>
        ))}
      </select>
      <input type="date" onChange={(e) => setDate(e.target.value)}></input>
      <button onClick={() => {getForecast(selectedLocation, date)}}>Submit</button>
    </div>
  );
}
