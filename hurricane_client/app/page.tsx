"use client";
import styles from "./hp.module.css";
import { useState } from "react";

type Location = {
  lon: number;
  lat: number;
};

export default function Home() {
  const pageTitle = "StormWatch"
  const [selectedLocation, setSelectedLocation] = useState("");
  const [date, setDate] = useState("");
  const [prediction, setPrediction] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const validLocations: Record<string, Location> = {
    "PA": { lon: -77.194527, lat: 41.2033 },
    "NY": { lon: -74.0060, lat: 40.7128 },
    "FL": { lon: -81.5158, lat: 27.6648 }
  };

  async function getForecast(location: Location, date: string) {
    if (!location || location.lon == undefined || location.lat == undefined) {
      console.log(`cannot use null values!!!!!!!!!~!`);
      return;
    }
    console.log(`Parameters: {loc: (${location.lon},${location.lat}), date: ${date}}`);
    try {
      setIsLoading(true);
      const dateTime = new Date(date).toISOString();
      console.log(dateTime);
      const res = await fetch(`/api/forecast`,
        {
          headers: {
            'Content-Type': 'application/json'
          }, method: 'POST',
          body: JSON.stringify({ date: dateTime, lon: validLocations[selectedLocation].lon, lat: validLocations[selectedLocation].lat })
        });
      if (!res.ok) {
        setError("Error fetching forecast, please try again.");
        return;
      }
      const json = await res.json();
      console.log(json);
      const prediction = await predict(json);
      setPrediction(prediction.body);
      console.log(prediction);
    }
    catch (err) {
      console.log("Error fetching forecast: ", err);
      setError("Error fetching forecast, please try again.");
    }
    finally {
      setIsLoading(false);
    }
  }

  async function predict(data: any) {
    const prediction = await fetch("/api/prediction", { headers: { 'Content-Type': 'application/json' }, method: 'POST', body: JSON.stringify({ forecast: data }) });
    const json = await prediction.json();
    return json;
  }
  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.card}>
          <div className={styles.title}>{pageTitle}</div>
          <div className={styles.selector}>
            <select required value={selectedLocation} onChange={(e) => setSelectedLocation(e.target.value)}>
              <option value="" disabled>Select a location</option>
              {Object.entries(validLocations).map(([key, value]) => (
                <option key={key} value={key}>
                  {key}
                </option>
              ))}
            </select>
            <input required type="date" onChange={(e) => setDate(e.target.value)} />
            <button onClick={() => { }}>Submit</button>
          </div>
          <div className={styles.loading_container}>
            <span>Loading...</span>
          </div>
        </div>
      </div>

    );
  }
  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.title}>{pageTitle}</div>
        <div className={styles.selector}>
          <select value={selectedLocation} onChange={(e) => setSelectedLocation(e.target.value)}>
            <option value="" disabled>Select a location</option>
            {Object.entries(validLocations).map(([key, value]) => (
              <option key={key} value={key}>
                {key}
              </option>
            ))}
          </select>
          <input type="date" onChange={(e) => setDate(e.target.value)} />
          <button onClick={() => { getForecast(validLocations[selectedLocation], date) }}>Submit</button>
        </div>
        {prediction && (<div className={styles.output}>{prediction}</div>)}
        {error && (<div className={styles.output}>
          {error}
        </div>)}
      </div>
    </div>
  );
}
