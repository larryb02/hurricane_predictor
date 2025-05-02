"use server";
import OpenAI from 'openai';
import dotenv from 'dotenv';
import { NextResponse } from "next/server";

dotenv.config();

export async function POST(request: any) {
    // Parse the request body
    const requestBody = await request.json();
    console.log(requestBody);  // This will log the parsed JSON request body
    const client = new OpenAI({
        apiKey: process.env['OPENAI_API_KEY'], // This is the default and can be omitted
        baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
    });

    const completion = await client.chat.completions.create({
        model: 'gemini-2.0-flash',
        messages: [
            { role: 'developer', content: 'You are a weather forecasting assistant with expertise in predicting hurricanes based on historical data and meteorological patterns.' },
            { role: 'user', content: 'Based on the current ocean temperature, atmospheric pressure, and wind patterns in Florida, how likely is it that a hurricane will form in the next month? Please provide your prediction based on general knowledge of these factors.' },
        ]
    });

    return NextResponse.json({ body: completion.choices[0].message.content }, { status: 200 });
}