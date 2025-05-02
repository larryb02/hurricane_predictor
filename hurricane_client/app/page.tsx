"use client";
import styles from "./hp.module.css";
import { useState } from "react";

type Location = {
  lon: number;
  lat: number;
};

export default function Home() {
  const [selectedLocation, setSelectedLocation] = useState("");
  const [date, setDate] = useState("");
  const [prediction, setPrediction] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const validLocations: Record<string, Location> = {
    "PA": { lon: -77.194527, lat: 41.2033 },
    "NY": { lon: -74.0060, lat: 40.7128 },
    "FL": { lon: -81.5158, lat: 27.6648 }
  };

  async function getForecast(location: Record<string, Location>, date: string) {
    console.log(`Parameters: {loc: (${location.lon},${location.lat}), date: ${date}}`);
    const dateTime = new Date(date).toISOString();
    // try {
    //   const dateTime = new Date(date).toISOString();
    //   console.log(dateTime);
    //   const res = await fetch(`http://35.221.13.68:8000/forecast`,
    //     {
    //       headers: {
    //         'Content-Type': 'application/json'
    //       }, method: 'POST',
    //       body: JSON.stringify({ date: dateTime, lon: validLocations[selectedLocation].lon, lat: validLocations[selectedLocation].lat })
    //     });
    //   const json = await res.json();
    //   // then just log the output 
    //   console.log(json);
    // }
    // catch (err) {
    //   console.log("Error fetching forecast: ", err);
    // }

    setIsLoading(true);
    const prediction = await fetch("/prediction", { headers: { 'Content-Type': 'application/json' }, method: 'POST', body: JSON.stringify({ date: dateTime, data: {} }) });
    const json = await prediction.json();
    console.log(json);
    setIsLoading(false);

  }
  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.card}>
          <div className={styles.title}>Hurricane Prediction Tool</div>
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
            <button onClick={() => { }}>Submit</button>
          </div>
          <div className={styles.loading_container}>
          Loading...
        </div>
        </div>
      </div>

    );
  }
  //   return (
  //     <div className="container">
  //       <div className="Title">
  //         Hurricane Prediction Tool
  //       </div>
  //       <div className="selector" style={styles.selector}>
  //         <select
  //           value={selectedLocation}
  //           onChange={(e) => setSelectedLocation(e.target.value)}>
  //           <option value="" disabled>
  //             Select a location
  //           </option>
  //           {Object.entries(validLocations).map(([key, value]) => (
  //             <option key={key} value={key}>
  //               {key}
  //             </option>
  //           ))}
  //         </select>
  //         <input type="date" onChange={(e) => setDate(e.target.value)}></input>
  //         <button onClick={() => { getForecast(validLocations[selectedLocation], date) }}>Submit</button>
  //       </div>
  //       <div className="Output">

  //       </div>
  //     </div>
  //   );
  // }
  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.title}>Hurricane Prediction Tool</div>
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
        <div className={styles.output}></div>
      </div>
    </div>
  );
}
