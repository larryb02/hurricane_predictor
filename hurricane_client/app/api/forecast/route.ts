"use server";
import { NextResponse } from "next/server";

export async function POST(req: any) {
    const reqBody = await req.json();
    console.log(JSON.stringify(reqBody));
    try {
        const response = await fetch("http://35.221.13.68:8000/forecast", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(reqBody),
        });

        const data = await response.json();
        return NextResponse.json(data);
    }
    catch (err) {
        console.log("Error fetching forecast: ", err);
        return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
    }

}