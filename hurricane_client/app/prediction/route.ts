"use server";
import OpenAI from 'openai';
import dotenv from 'dotenv';
import { NextResponse } from "next/server";

dotenv.config();

export async function POST(request: any) {
    // Parse the request body
    const requestBody = await request.json();
    console.log(requestBody);
    console.log(JSON.stringify(requestBody.forecast));  // This will log the parsed JSON request body
    const client = new OpenAI({
        apiKey: process.env['OPENAI_API_KEY'], // This is the default and can be omitted
        baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
    });

    const completion = await client.chat.completions.create({
        model: 'gemini-2.0-flash',
        messages: [
            { role: 'developer', content: 'You are a weather forecasting assistant with expertise in predicting hurricanes based on forecasted data given to you. Determine the probability of a hurricane occurring. Use the following format to provide the probability \'There is a %x chance of a tropical storm occuring!\', we do NOT need an explanation.' },
            { role: 'user', content: `Forecasted data in json: ${JSON.stringify(requestBody.forecast)}` },
        ]
    });
    console.log(completion.choices[0].message.content);
    return NextResponse.json({ body: completion.choices[0].message.content }, { status: 200 });
}