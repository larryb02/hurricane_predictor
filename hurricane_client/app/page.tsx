import Image from "next/image";
import styles from "./page.module.css";
import {useState} from "react";

export default function Home() {
  const validLocations = {}; // key = location_name, value = (long,lat)
  return (
    <div className={styles.page}>
      "Select a location"
      <select>
        <option>PA</option>
        <option>NY</option>
        <option>NJ</option>
      </select>
    </div>
  );
}
